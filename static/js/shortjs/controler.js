var ShortenerView = Backbone.View.extend({
    el: $('#_container'),
    attributes: {
        'class': ''
    },
    recentURLTimer: null, //5 sec poll for new urls and clicks
    initialize: function(){
        _.bindAll(this, 'render',
            'getShortURL',
            'setRecentShortsTimer'
        );

        var _this = this;

        this.short_url_model = new Short_URL_Model();
        this.recent_shorts_model = new Recent_Shorts_Model(recent_urls_bootstrap);
    },
    setRecentShortsTimer: function(){
        var _this = this;
        clearTimeout(this.recentURLTimer);
        this.recentURLTimer = setTimeout(function(){
                _this.checkRecentShorts();
        }, 5000);
    },
    checkRecentShorts: function(){
    }
        
        
});



jQuery(document).ready(function($) {
    shortenerView = new ShortenerView();
});
