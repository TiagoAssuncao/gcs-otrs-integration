$(function () {

  /* Functions */

  var loadUpdateForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
        $("#LoadingImage").show();

      },
      success: function (data) {
          $("#modal-book .modal-content").html(data.html_form);
        $("#LoadingImage").hide();
      },
      error: function(data){
	sweetAlert("Oops...", "Something went wrong!", "error");
        // alert("Não foi possivel executar a ação!");
        $("#modal-book").modal("hide");
        $("#LoadingImage").hide();
      }
    });
  };

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
        $("#LoadingImage").show();

      },
      success: function (data) {
	if(typeof modalbook === 'undefined'){
		modalbook = $("#modal-book .modal-content").html(data.html_form);
	} else {
		$("#modal-book").modal("show");
	}
        $("#LoadingImage").hide();
      },
      error: function(data){
	sweetAlert("Oops...", "Something went wrong!", "error");
        // alert("Não foi possivel executar a ação!");
        $("#modal-book").modal("hide");
        $("#LoadingImage").hide();
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      beforeSend: function () {
        $("#LoadingImage").show();
      },
      success: function (data) {
          $("#modal-book").modal("hide");
          $("#LoadingImage").hide();
          // alert("GSC Atualizado com sucesso!");
	swal({
	  title: "Atualizado!",
	  text: "GCS atualizado com sucesso!",
	  type: "success",
	  confirmButtonText: "Ok!",
	  closeOnConfirm: false,
	  closeOnCancel: false
	},
	function(isConfirm){
		 document.location.reload();
	});
      },
      error: function(data){
	sweetAlert("Oops...", "Não foi possível executar a ação", "error");
        // alert("Não foi possivel executar a ação!");
        $("#modal-book").modal("hide");
        $("#LoadingImage").hide();
      }
    });
    return false;
  };



  var progressForm = function () {
    var btn = $(this);
    $("#LoadingImage").show();
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#LoadingImage").show();
      },
      success: function (data) {
        $("#LoadingImage").hide();
        // alert("Banco de Dados Atualizado com sucesso!");
	// swal("Good job!", "Banco de Dados atualizado com Sucesso!", "success");
	swal({
	  title: "Atualizado!",
	  text: "Base de dados atualizada com Sucesso!",
	  type: "success",
	  confirmButtonText: "Ok!",
	  closeOnConfirm: false,
	  closeOnCancel: false
	},
	function(isConfirm){
		 document.location.reload();
	});
      },
      error: function(data){
	sweetAlert("Oops...", "Não foi possível executar a ação", "error");
        // alert("Não foi possivel executar a ação!");
        $("#LoadingImage").hide();
      }
    });
  };




  /* Binding */

  $(".js-create-book").click(loadForm);
  $(".js-update-book").click(loadUpdateForm);
  $(".js-database-book").click(progressForm);
  $("#modal-book").on("submit", ".js-book-create-form", saveForm);

});
