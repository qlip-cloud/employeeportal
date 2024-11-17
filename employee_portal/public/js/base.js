$(document).ready(function () {
    $('.module-link').on('click', function (event) {
        event.preventDefault();
        let url = $(this).data('url');

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

                $(response).find('script').each(function () {
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

                history.pushState(null, '', url);
            },
            error: function () {
                console.error("Error al cargar el contenido.");
            }
        });
    });
    
});

new DataTable('#table-endowments');
new DataTable('#table-documents');
new DataTable('#table-evaluations');
new DataTable('#table-leaves');