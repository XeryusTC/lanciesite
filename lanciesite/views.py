from django.views.generic import TemplateView

class BaseStyleView(TemplateView):
    template_name = "lanciesite/style.css"

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        left_menu_width = 190
        right_menu_width = 120
        base_padding = 10
        page_padding = 15
        menu_width = (left_menu_width + right_menu_width + base_padding * 4 + page_padding * 2 + 16)
        near_white = "#f5f5f5"

        # add all the different options to the template context so that they are accessible from within the css template
        # TODO: sort these in a sensible way
        context.update([
            ("base_background",     "#3b3b3b"),
            ("light_background",    near_white),
            ("base_foreground",     "white"),
            ("dark_foreground",     "black"),
            ("light_foreground",    near_white),
            ("base_fonts",          "verdana, sans, sans-serif"),
            ("page_padding",        page_padding),
            ("base_padding",        base_padding),
            ("border_radius",       5),
            ("left_column_width",   left_menu_width + base_padding * 2),
            ("column_padding",      base_padding),
            ("right_column_width",  right_menu_width + base_padding * 2),
            ("page_max_width",      1920 - menu_width),
            ("page_min_width",      1024 - menu_width),
            ("base_link_color",     near_white),
            ("shadow_color",        "black"),
            ("shadow_color_light",  "#333"),
            ("content_bottom_space",2 * page_padding),
            ("light_link_color",    "#004274"),
            ("navbar_background",   "#a90707"),
            ("navbar_height",       40),
            ("navbar_list_padding", base_padding / 2),
            ("navbar_active_bg",    "rgba(0, 0, 0, 0.1)"),
            ("left_menu_width",     left_menu_width),
            ("right_menu_width",    right_menu_width),
            ("menu_item_padding",   10),
            ("menu_item_spacing",   base_padding),
            ("menu_header_color",   "#b80a0a"),
        ])

        return context

    def render_to_response(self, context, **kwargs):
        return super(TemplateView, self).render_to_response(context, content_type="text/css", **kwargs) # override the MIME type
