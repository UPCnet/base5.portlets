$(document).ready(function() {

  // Call the ws that stores the span value given a portletManager
  $('.editable').bind('change', function(event) {
    // event.preventDefault()
    // event.stopPropagation()
    data = {'manager': $(this).data()['manager'],
            'contextId': $(this).data()['contextId'],
            'col': $(this).val()};
    $.ajax({
      url: data.contextId + "/@@set-portlet-cols",
      data: data,
      type: 'POST',
      success: function(data){
          alertify.success("Configuració guardada.");
      },
      error: function(){
          alertify.error("Error al guardar la configuració.");
      }
    });
  });
});
