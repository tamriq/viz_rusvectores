$(function() {
    var checkbox = $('input[id=high]');

    checkbox.click(function() {
        if (this.checked) {
            $("li.high").fadeIn('slow');
        } else {
            $("li.high").fadeOut('slow');
        }
    });
});

$(function() {
    var checkbox = $('input[id=mid]');

    checkbox.click(function() {
        if (this.checked) {
            $("li.mid").fadeIn('slow');
        } else {
            $("li.mid").fadeOut('slow');
        }
    });
});

$(function() {
    var checkbox = $('input[id=low]');

    checkbox.click(function() {
        if (this.checked) {
            $("li.low").fadeIn('slow');
        } else {
            $("li.low").fadeOut('slow');
        }
    });
});