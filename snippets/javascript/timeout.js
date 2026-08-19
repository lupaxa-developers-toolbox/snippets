// snippet:
// title: "Warn before a session timeout"
// card_title: "Session timeout modal"
// summary: "A jQuery plugin that starts a session timer, shows a stay-signed-in modal after inactivity, and redirects to a logout URL if the user does not respond."
// tags: [timeout, session]
// added: "2026-08-19T09:20:00+01:00"
// submitted_by: Lupraxus
// runnable: false
// caveats: "Needs jQuery and Bootstrap 3 modal markup (data-dismiss, .modal('show')). Set logouturl or the plugin does nothing."
// end-snippet
(function ($, document, window) {
    "use strict";

    $.fn.userTimeout = function (opts) {
        var defaults = {
            logouturl: null,
            notify: true,
            timer: true,
            session: 600000,
            force: 300000,
            debug: false,
            modalTitle: "Session Timeout",
            modalBody:
                "You're being timed out due to inactivity. Please choose to stay signed in or to logoff. Otherwise, you will logged off automatically.",
        };

        var options = $.extend(defaults, opts || {});
        var timeout;
        var forceLogout;
        var countDownTimer;
        var seconds = Math.floor((options.force / 1000) % 60);

        var init = function () {
            clearTimeout(timeout);

            if (!options.logouturl) {
                if (options.debug === true) {
                    window.alert("Please configure the userTimeout plugin!");
                }
                return;
            }

            resetTime(false);

            $(document).on("click mousemove mousedown keyup scroll keypress", function () {
                resetTime(false);
            });
        };

        var modal = function () {
            resetTime(true);

            if (options.timer === false) {
                $(document).on("click mousemove mousedown keyup scroll keypress", function () {
                    resetTime(true);
                });
            } else {
                $(document).off();
            }

            var container = $('<div class="modal fade" id="notifyLogout"></div>');
            var dialog = $('<div class="modal-dialog"></div>');
            var content = $('<div class="modal-content"></div>');
            var header = $(
                '<div class="modal-header"><h4 class="modal-title" id="notifyLogoutLabel">' +
                    options.modalTitle +
                    '</h4><button type="button" class="close" data-dismiss="modal">&times;</button></div>'
            );
            var body = $('<div class="modal-body">' + options.modalBody + "</div>");
            var footer;
            var logoutBtn;

            if (options.timer === true) {
                footer = $(
                    '<div class="modal-footer"><button type="button" class="btn btn-primary" data-dismiss="modal">Stay Logged In (<span id="countdowntimer">' +
                        seconds +
                        "</span>)</button></div>"
                );
                countDown(seconds);
            } else {
                footer = $(
                    '<div class="modal-footer"><button type="button" class="btn btn-primary" data-dismiss="modal">Stay Logged In</button></div>'
                );
            }

            logoutBtn = $('<button type="button" class="btn btn-default" id="logoff">Log Off</button>');

            content.append(header, body, footer);
            footer.prepend(logoutBtn);
            dialog.append(content);
            container.append(dialog);

            $(container).modal("show");

            $(container).on("hide.bs.modal", function () {
                resetTime(false);

                $(document).on("click mousemove mousedown keyup scroll keypress", function () {
                    resetTime(false);
                });

                $(container).remove();
            });

            $(logoutBtn).on("click", function () {
                logout();
            });
        };

        var countDown = function (countTime) {
            $("#countdowntimer").html(countTime);

            if (countTime !== 0) {
                countDownTimer = setTimeout(function () {
                    countDown(countTime - 1);
                }, 1000);
            } else {
                clearTimeout(countDownTimer);
            }
        };

        var resetTime = function (modaltime) {
            clearTimeout(timeout);
            clearTimeout(forceLogout);
            clearTimeout(countDownTimer);

            if (modaltime === true) {
                forceLogout = setTimeout(logout, options.force);
            } else if (options.notify === true) {
                timeout = setTimeout(modal, options.session);
            } else {
                timeout = setTimeout(logout, options.session);
            }
        };

        var logout = function () {
            clearTimeout(timeout);
            clearTimeout(forceLogout);
            clearTimeout(countDownTimer);
            window.location = options.logouturl;
        };

        return this.each(function () {
            init();
        });
    };
}(jQuery, document, window));
