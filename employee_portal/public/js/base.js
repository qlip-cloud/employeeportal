$(document).ready(function () {
  function loadModule(url) {
    $('#dynamic-content').fadeOut(150, function () {
      $.ajax({
        url: url,
        method: 'GET',
        success: function (response) {
          let newContent = $(response).find('#dynamic-content').html();

          $('#dynamic-content').html(newContent).fadeIn(150);

          $(response).find('link[rel="stylesheet"]').each(function () {
            let href = $(this).attr('href');
            if (!$(`link[href="${href}"]`).length) {
              $('<link>', { rel: 'stylesheet', href: href }).appendTo('head');
            }
          });

          let scripts = $(response).find('script[src]').map(function () {
            return $(this).attr('src');
          }).get();

          loadScriptsSequentially(scripts, function () {
            $(response).find('script:not([src])').each(function () {
              $.globalEval(this.textContent || this.innerText);
            });
          });

          history.pushState(null, '', url);
          attachModuleEvents();
        },
        error: function (xhr, status, error) {
          console.error("Error al cargar el contenido: ", error);
          $('#dynamic-content').fadeIn(150);
        }
      });
    });
  }

  function loadScriptsSequentially(scripts, callback) {
    function loadNext(index) {
      if (index < scripts.length) {
        $.getScript(scripts[index], function () {
          loadNext(index + 1);
        });
      } else if (typeof callback === "function") {
        callback();
      }
    }
    loadNext(0);
  }

  function attachModuleEvents() {
    $('.module-link').off('click').on('click', function (event) {
      event.preventDefault();
      let url = $(this).data('url');
      loadModule(url);
    });
  }

  attachModuleEvents();
});
