
$(document).ready(function() {
  const router = new Router({
    contentSelector: '#dynamic-content',
    linkSelector: '.module-link',
    activeClass: 'active',
    fadeSpeed: 150
  });

  initMenuToggle();
  
  window.appRouter = router;
});


function initMenuToggle() {
  $("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("menuDisplayed");
    
    let icon = $(this).find("span");
    if ($("#wrapper").hasClass("menuDisplayed")) {
      icon.text("menu_open");
    } else {
      icon.text("menu");
    }
  });
}

window.AppUtils = {
  navigateTo: function(url) {
    if (window.appRouter) {
      window.appRouter.goTo(url);
    }
  },
  
  getCurrentRoute: function() {
    return window.appRouter ? window.appRouter.getCurrentRoute() : '';
  },
  
  isLoading: function() {
    return window.appRouter ? window.appRouter.isNavigating() : false;
  },
  
  showNotification: function(message, type = 'info') {
    const alertClass = type === 'success' ? 'alert-success' : 
                      type === 'error' ? 'alert-danger' : 
                      type === 'warning' ? 'alert-warning' : 'alert-info';
    
    const toast = $(`
      <div class="alert ${alertClass} alert-dismissible fade show" 
           style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
        ${message}
        <button type="button" class="close" data-dismiss="alert">
          <span>&times;</span>
        </button>
      </div>
    `);
    
    $('body').append(toast);
    
    setTimeout(() => {
      toast.fadeOut(() => toast.remove());
    }, 5000);
  },
  
  validateForm: function($form) {
    let isValid = true;
    
    $form.find('[required]').each(function() {
      const $field = $(this);
      if (!$field.val().trim()) {
        $field.addClass('is-invalid');
        isValid = false;
      } else {
        $field.removeClass('is-invalid');
      }
    });
    
    return isValid;
  }
};

function attachModuleEvents() {
  if (window.appRouter) {
    window.appRouter.attachEvents();
  }
}