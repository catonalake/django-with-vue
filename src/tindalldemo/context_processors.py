# do this as a context processor is that it is available on any template
from django.conf import settings

def vue_js_files(request):
    static_base_dir = settings.STATICFILES_BASE_DIR
    vue_dir = 'vue-prod' if settings.VUE_PROD else 'vue-dev'
    vue_dir = static_base_dir / vue_dir / "assets"
    js_files = [x.relative_to(static_base_dir) for x in vue_dir.glob("**/*.js")]
    css_files = [x.relative_to(static_base_dir) for x in vue_dir.glob("**/*.css")]
    print(str(js_files))
    print(str(css_files))
    return {
        "vue_js_paths": list(js_files),
        "vue_css_paths": list(css_files),
    }
