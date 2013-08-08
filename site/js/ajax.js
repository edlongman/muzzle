/*****************************************************************************/
/*                        Get JSON response from PHP                         */
/*****************************************************************************/

function getGuardianNews(amount, scope, section, keyword){
    today = new Date(); // dates are entered relatively, today is needed

    start_time = new Date();
    end_time = today;
    //section = section;

    // get correct start time
    switch (scope) {
        case 'days': start_time.setDate(today.getDate()-amount); break;
        case 'weeks': start_time.setDate(today.getDate()-amount*7); break;
        case 'months': start_time.setMonth(today.getMonth()-amount); break;
    }

    // make asynchronous ajax request, calls handle
    ajaxGuardian(start_time, end_time, section, keyword);
}

function ajaxGuardian(start_time, end_time, section, keyword){
    $.ajax({
        url: 'include.php',
        type: 'GET',
        dataType: 'json',
        data: {start_time: start_time.f('yyyy-MM-dd'), end_time: end_time.f('yyyy-MM-dd'), section: section, keyword: keyword},
        success: function(data, textStatus, xhr) {
            // replace JSON date format with JavaScript Date Objects
            $.each(data[0], function(index, story) {
                 story[2] = new Date(story[2]);
            });

            // call handleGuardianNews function of whileaway.js
            handleGuardianNews(data[0]);
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log('ERROR: ' + errorThrown);
        }
    });
}
