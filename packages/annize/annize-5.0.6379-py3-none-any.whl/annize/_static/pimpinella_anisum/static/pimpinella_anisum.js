/*
* SPDX-FileCopyrightText: © 2020 Josef Hahn
* SPDX-License-Identifier: AGPL-3.0-only
*/

"use strict";

$(document).ready(function() {

    $('.body').find('a').not('[class*=internal]').attr('target', '_blank');

    document.body.classList.add('scripted');

});
