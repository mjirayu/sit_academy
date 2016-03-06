define(["ckeditor", 'js/utils/handle_iframe_binding', "utility"],
    function(CKEditor, IframeBinding) {
        var editWithCKEditor = function(model, contentName, baseAssetUrl, textArea, id) {
            var content = rewriteStaticLinks(model.get(contentName), baseAssetUrl, '/static/');
            model.set(contentName, content);

            var $codeMirror = CKEditor.instances[id];

            if ($codeMirror) {
              $codeMirror.destroy(true);
            }

            $codeMirror = CKEditor.replace(textArea.id);
            $codeMirror.on('change', function () {
                    $('.save-button').removeClass('is-disabled').attr('aria-disabled', false);
            });
            $codeMirror.setData(content);
            $codeMirror.on('setData', function(e) {
              $codeMirror.resetUndo();
            });

            return $codeMirror;
        };

        var changeContentToPreview = function (model, contentName, baseAssetUrl) {
            var content = rewriteStaticLinks(model.get(contentName), '/static/', baseAssetUrl);
            // Modify iframe (add wmode=transparent in url querystring) and embed (add wmode=transparent as attribute)
            // tags in html string (content) so both tags will attach to dom and don't create z-index problem for other popups
            // Note: content is modified before assigning to model because embed tags should be modified before rendering
            // as they are static objects as compared to iframes
            content = IframeBinding.iframeBindingHtml(content);
            model.set(contentName, content);
            return content;
        };

        return {'editWithCKEditor': editWithCKEditor, 'changeContentToPreview': changeContentToPreview};
    }
);
