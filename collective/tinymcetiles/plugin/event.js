;(function($) {

    // Init on load
    $(window).load(function () {

        // Check if tiledata is available and valid
        if (typeof(tiledata) !== 'undefined') {

            // Get object
            var w =  window.dialogArguments || opener || parent || top;
            tinymce = w.tinymce;
            editor = tinymce.EditorManager.activeEditor;

            // Check action
            if (tiledata.action == 'cancel') {

                // Close dialog
                editor.windowManager.close(window);

            } else if (tiledata.action == 'save') {

                // Check url
                if (typeof(tiledata.url) !== 'undefined') {

                    // Insert content
                    editor.execCommand('mceInsertContent', false, editor.dom.createHTML('img', {
                        src : '/++resource++collective.tinymcetiles.plugin/placeholder.gif',
                        alt : tiledata.url,
                        class : 'mceItem mceTile',
                        border : 0
                    }));

                    // Close popup
                    editor.windowManager.close(window);
                }
            }
        }
    });
})(jQuery);
