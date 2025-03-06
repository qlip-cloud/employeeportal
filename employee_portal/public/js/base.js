$(document).ready(function () {
    function loadModule(url) {
        $('#dynamic-content').html('<div class="loading-message">Cargando...</div>');

        $.ajax({
            url: url,
            method: 'GET',
            success: function (response) {
                let newContent = $(response).find('#dynamic-content').html();
                $('#dynamic-content').html(newContent);

                $(response).find('link[rel="stylesheet"]').each(function () {
                    let href = $(this).attr('href');
                    if (!$(`link[href="${href}"]`).length) {
                        $('<link>', { rel: 'stylesheet', href: href }).appendTo('head');
                    }
                });
                $(response).find('script[src]').each(function () {
                    let src = $(this).attr('src');
                    if (src && !$(`script[src="${src}"]`).length) {
                        $.getScript(src);
                    }
                });

                $(response).find('script:not([src])').each(function () {
                    $.globalEval(this.textContent || this.innerText);
                });
                if (url.includes('my_profile')) {
                    if (typeof initializeEmployeeForm === 'function') {
                        initializeEmployeeForm();
                    }
                }

                // Actualizar la URL sin recargar la página
                history.pushState(null, '', url);

                // Volver a vincular los eventos para los submódulos después de la carga
                attachModuleEvents();
            },
            error: function () {
                console.error("Error al cargar el contenido.");
                $('#dynamic-content').html('<div class="error-message">Error al cargar el módulo.</div>');
            }
        });
    }

    function attachModuleEvents() {
        $('.module-link').off('click').on('click', function (event) {
            event.preventDefault();
            let url = $(this).data('url');
            loadModule(url);
        });
    }

    // Enlazar eventos iniciales
    attachModuleEvents();
});
