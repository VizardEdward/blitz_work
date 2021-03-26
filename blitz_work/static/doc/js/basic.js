
$(document).ready(function(){
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
    });
});