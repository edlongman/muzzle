/*****************************************************************************/
/*                          Main JS for whileaway                            */
/*****************************************************************************/

$(document).ready(function(){
    $('#form').on('submit', function(e){
        e.preventDefault();

        amount = $('#number').val();
        scope = $('#date option:selected').val();
        keyword = $('#keyword option:selected').val();
        if (keyword == 'news') {
            keyword = '';
        };

        try {
            validate(amount, scope, keyword);
        } catch (e) {
            alert(e);
            return;
        }

        // make asynchronous request
        getNews(amount, scope, keyword);
    });
});

function handleNews(news){
    test(news);
}

function test(response){
    str = '<ul>';
    for (var i = 0; i < response[0].length; i++) {
        str += '<li>' + response[0][i] + ': <a href="' + response[1][i] + '">' + response[1][i] + '</a></li>';
    };
    str += '</ul>'
    $('#test').html(str);
}

function validate(amount, scope, keyword) {
    scopes = ['days', 'weeks', 'months'];
    if (scopes.indexOf(scope) < 0) {
        throw 'Invalid scope';
    }

    if (isNaN(amount)) {
        throw 'Invalid amount';
    }

    $.trim(keyword);
}