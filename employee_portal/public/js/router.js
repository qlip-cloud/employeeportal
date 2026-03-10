class Router {
  constructor(options = {}) {
    this.options = {
      contentSelector: '#dynamic-content',
      linkSelector: '.module-link',
      activeClass: 'active',
      fadeSpeed: 150,
      ...options
    };
    
    this.loadedScripts = new Set();
    this.currentRoute = '';
    this.isLoading = false;
    
    this.init();
  }

  init() {
    this.handlePopState();
    this.attachEvents();
    this.highlightCurrentRoute();
  }

  handlePopState() {
    window.addEventListener('popstate', (event) => {
      const path = window.location.pathname;
      this.loadModule(path, false);
    });
  }

  attachEvents() {
    $(document).off('click', this.options.linkSelector);
    $(document).on('click', this.options.linkSelector, (event) => {
      event.preventDefault();
      
      if (this.isLoading) return;
      
      const $link = $(event.currentTarget);
      const url = $link.data('url') || $link.attr('href');
      
      if (url && url !== this.currentRoute) {
        this.updateActiveState($link);
        this.loadModule(url, true);
      }
    });
  }

  updateActiveState($clickedLink) {
    $('.sidebar-nav li').removeClass(this.options.activeClass);
    $clickedLink.parent().addClass(this.options.activeClass);
  }

  highlightCurrentRoute() {
    const currentPath = window.location.pathname.replace(/\/+$/, '');
    document.querySelectorAll('.sidebar-nav li a').forEach(link => {
      if (link.getAttribute('href').replace(/\/+$/, '') === currentPath) {
        link.parentElement.classList.add(this.options.activeClass);
      }
    });
  }

  loadModule(url, addToHistory = true) {
    if (this.isLoading) return;
    
    this.isLoading = true;
    const $content = $(this.options.contentSelector);
    
    console.log('Loading:', url);
    
    $content.fadeOut(this.options.fadeSpeed, () => {
      $.ajax({
        url: url,
        method: 'GET',
        timeout: 10000,
        success: (response) => {
          this.processResponse(response, $content, url, addToHistory);
        },
        error: (xhr, status, error) => {
          console.error("Error al cargar el contenido:", error);
          this.showError($content, xhr.status);
          this.isLoading = false;
        }
      });
    });
  }

  processResponse(response, $content, url, addToHistory) {
    const $response = $(response);
    
    let newContent = $response.find(this.options.contentSelector).html();
    
    if (newContent) {
      $content.html(newContent);
      
      this.finishLoading($content, url, addToHistory);

    } else {
      console.warn('No se encontró contenido en la respuesta');
      this.finishLoading($content, url, addToHistory);
    }
  }

  finishLoading($content, url, addToHistory) {
    if (addToHistory && url !== window.location.pathname) {
      history.pushState(null, '', url);
    }
    
    this.currentRoute = url;
    $content.fadeIn(this.options.fadeSpeed);
    this.attachEvents();
    this.isLoading = false;
    $(document).trigger('router:page_loaded', [url]);
  }

  showError($content, status) {
    let message = 'Error al cargar el contenido';
    
    if (status === 404) message = 'Página no encontrada';
    if (status === 403) message = 'Sin permisos para acceder';
    if (status === 500) message = 'Error del servidor';
    
    $content.html(`
      <div class="alert alert-danger text-center" style="margin: 50px auto; max-width: 500px;">
        <h4>Error ${status}</h4>
        <p>${message}</p>
        <button class="btn btn-primary" onclick="location.reload()">
          Recargar Página
        </button>
      </div>
    `).fadeIn(this.options.fadeSpeed);
  }


  goTo(url) {
    if (this.isLoading) return;
    $('.sidebar-nav li').removeClass(this.options.activeClass);
    $(this.options.linkSelector).each(function() {
      const linkUrl = $(this).data('url') || $(this).attr('href');
      if (linkUrl === url) {
        $(this).parent().addClass('active');
      }
    });
    
    this.loadModule(url, true);
  }

  getCurrentRoute() {
    return this.currentRoute;
  }

  isNavigating() {
    return this.isLoading;
  }
}