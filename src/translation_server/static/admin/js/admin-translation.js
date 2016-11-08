/**
 * Created by gdelnegro on 10/1/16.
 */
var method = undefined;
var lastTranslationTagUrl = undefined;
var translationTypeUrl = undefined
document.onreadystatechange = function () {
  if (document.readyState === "complete") {
      document.getElementById('id_tag').readOnly = true;
      document.getElementById('id_auxiliary_tag').readOnly = true;
      jQuery(".field-last_tag").children('div').children('p').text("");
      translationTypeUrl = document.getElementById('id_translation_type_url').value;
      lastTranslationTagUrl = document.getElementById('id_last_translation_tag_url').value;
      if (document.URL.indexOf("add") > -1){
          method = "add";
          document.getElementById("id_type").addEventListener("change", onChangeTranslationType);
      }else if(document.URL.indexOf("change") > -1){
          protectFields();
          onChangeTranslationType();
          method = "edit";
      }
  }
};

/**
 * show/hide fields
 */
function showFields(){
    jQuery(".field-auxiliary_tag").show();
    jQuery('[class*=" field-auxiliary_text_"]').parents(".ui-tabs").show();
}

function hideFields(){
    jQuery(".field-auxiliary_tag").hide();
    jQuery('[class*=" field-auxiliary_text_"]').parents(".ui-tabs").hide();
}

/**
 * Keep fields from being edited
 */
function protectFields(){
    var ids = ["id_tag", "id_type", "id_auxiliary_tag"]
    for(var i=0; i<ids.length;i++){
        jQuery("#"+ids[i]).prop('readonly', true);
    }
    jQuery("#add_id_type").hide();
    jQuery("#change_id_type").hide();
}

function onChangeTranslationType(){
    if(jQuery("#id_type").val().length > 0){
        getTranslationTypeDetails()
    }
}

function getTranslationTypeDetails(){
    if(jQuery("#id_type").val().length > 0){
        var flag = false;
        var auxiliary_tag = null;
        jQuery.ajax({
            url: lastTranslationTagUrl+jQuery("#id_type").val(),
            context: document.body,
            async: false,
            success: function (data) {
                if (Object.keys(data.result).length > 0){
                    var result = data.result;
                    if(method == "add"){
                        jQuery(".field-last_tag").children('div').children('p').text(result.last_tag);
                        if(!jQuery("#id_tag").prop("disabled")){
                            jQuery("#id_tag").val(result.tag + (parseInt(result.last_id)+1));
                        }
                        if (result.has_auxiliary_text){
                            showFields();
                            jQuery("#id_auxiliary_tag").val(result.auxiliary_tag+(parseInt(result.last_id)+1))
                        }else{
                            hideFields();
                        }
                    }else if(method == "edit"){
                        if (result.has_auxiliary_text){
                            showFields();
                        }else{
                            hideFields();
                        }
                    }
                }else{
                    jQuery.ajax({
                        url: translationTypeUrl,
                        data:{id:jQuery("#id_type").val()},
                        async:false,
                        success: function (data){
                            result = data[0]
                            if(Object.keys(result).length > 0){
                                if(!jQuery("#id_tag").prop("disabled")){
                                    jQuery("#id_tag").val(result.tag + 1);
                                }
                                if (result.has_auxiliary_text){
                                    showFields();
                                    jQuery("#id_auxiliary_tag").val(result.auxiliary_tag+1)
                                }else{
                                    hideFields();
                                }
                            }
                        }
                    })
                }
            }
        });
        return [flag, auxiliary_tag];
    }else{
        clearFields();
        hideFields();
    }
}

function clearFields(){
    jQuery("#id_tag").val("");
    jQuery("#id_auxiliary_tag").val("");
    jQuery('[id*=" field-auxiliary_text_"]').val("");
}