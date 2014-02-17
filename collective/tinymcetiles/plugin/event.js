if (typeof String.prototype.startsWith != 'function') {
  // see below for better implementation!
  String.prototype.startsWith = function (str){
    return this.indexOf(str) == 0;
  };
}


var qs = (function(url) {
    var a = url.slice(url.indexOf('?') + 1).split('&');
    if (a == "") return {};
    var b = {};
    for (var i = 0; i < a.length; ++i)
    {
        var p=a[i].split('=');
        if (p.length != 2) continue;
        b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
    }
    return b;
});

(function ($) {

    // Init on load
    $(window).load(function () {

        // Check if tiledata is available and valid
        if (typeof(tiledata) !== 'undefined') {
            // tiledata is added by plone.app.tiles.browser.add
            // 1. popup created by editor_plugin.js with iframe to @@add-tile
            // 2. each page load of that iframe executes this code
            // 3. final page is @@add-tile/TILEID which has tiledata object

            // Get object
            var w = window.dialogArguments || opener || parent || top;
            tinymce = w.tinymce;
            editor = tinymce.EditorManager.activeEditor;

            // Check action
            if (tiledata.action == 'cancel') {

                // Close dialog
                editor.windowManager.close(window);

            } else if (tiledata.action == 'save') {

                // Check url
                if (typeof(tiledata.url) !== 'undefined') {
                    var name = tiledata.url;
                    if  (name.startsWith('./@@')) {
                        name = name.substring(4);
                    }
                    var allvars = qs(name);
                    name = name.slice(0, name.indexOf('?'));
                    var params = "";
                    for (var key in allvars) {
                        params += ' '+key+'="'+allvars[key]+'"';
                    }

                    $.ajax({
                        url: tiledata.url,
                        success: function(response) {
                            var shortcode = '[' + name + params+']';
                            shortcode += response;
                            shortcode += '[/' + name + ']';
                            // Insert content
                            editor.execCommand(
                                'mceInsertContent',
                                false,
                                editor.dom.createHTML(
                                    'p', {class: 'mceItem mceTile'}, shortcode));
                            // Close popup
                            editor.windowManager.close(window);
                        }
                    });


                }
            }
        }
    });
})(jQuery);
