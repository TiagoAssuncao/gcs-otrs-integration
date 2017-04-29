$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
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
          alert("GSC Atualizado com sucesso!");
          document.location.reload();
      },
      error: function(data){
        alert("Não foi possivel executar a ação.");
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
        alert("Banco de Dados Atualizado com sucesso!");
        document.location.reload();
      }
    });
  };




  /* Binding */

  // Create book
  $(".js-create-book").click(loadForm);
  // $("#modal-book").on("submit", ".js-book-create-form", saveForm);

  // Update book
  $(".js-database-book").click(progressForm);
  // $("#book-table").on("click", ".js-database-book", progressForm);
  $("#modal-book").on("submit", ".js-book-create-form", saveForm);

  // // Delete book
  // $("#book-table").on("click", ".js-delete-book", loadForm);
  // $("#modal-book").on("submit", ".js-book-delete-form", saveForm);

});
