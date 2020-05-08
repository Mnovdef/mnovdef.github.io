function hideArmors() {
    var armoredCheckbox = document.getElementById('ArmoredCheckbox');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        if ("Armored".localeCompare(images[index].dataset.move) === 0){
            if (armoredCheckbox.checked === true) {
                images[index].style.display = 'inline';
            } else {
                images[index].style.display = 'none';
            }
        }
    }
}


function hideFlying() {
    var flyingCheckbox = document.getElementById('FlyingCheckbox');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        if ("Flying".localeCompare(images[index].dataset.move) === 0){
            if (flyingCheckbox.checked === true) {
                images[index].style.display = 'inline';
            } else {
                images[index].style.display = 'none';
            }
        }
    }
}

function hideInfantry() {
    var infantryCheckbox = document.getElementById('InfantryCheckbox');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        if ("Infantry".localeCompare(images[index].dataset.move) === 0){
            if (infantryCheckbox.checked === true) {
                images[index].style.display = 'inline';
            } else {
                images[index].style.display = 'none';
            }
        }
    }
}

function hideCavalry() {
    var cavalryCheckbox = document.getElementById('CavalryCheckbox');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        if ("Cavalry".localeCompare(images[index].dataset.move) === 0){
            if (cavalryCheckbox.checked === true) {
                images[index].style.display = 'inline';
            } else {
                images[index].style.display = 'none';
            }
        }
    }
}

function hideLegend() {
    var legendCheckbox = document.getElementById('LegendCheckbox');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        if ("true".localeCompare(images[index].dataset.legend) === 0){
            if (legendCheckbox.checked === true) {
                images[index].style.display = 'inline';
            } else {
                images[index].style.display = 'none';
            }
        }
    }
}

function hideGrail() {
    var grailCheckbox = document.getElementById('GrailCheckbox');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        if ("true".localeCompare(images[index].dataset.grail) === 0){
            if (grailCheckbox.checked === true) {
                images[index].style.display = 'inline';
            } else {
                images[index].style.display = 'none';
            }
        }
    }
}

function hideSeasonal() {
    var seasonalCheckbox = document.getElementById('SeasonCheckbox');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        if ("true".localeCompare(images[index].dataset.season) === 0){
            if (seasonalCheckbox.checked === true) {
                images[index].style.display = 'inline';
            } else {
                images[index].style.display = 'none';
            }
        }
    }
}

function hideDuo() {
    var duoCheckbox = document.getElementById('DuoCheckbox');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        if ("true".localeCompare(images[index].dataset.duo) === 0){
            if (duoCheckbox.checked === true) {
                images[index].style.display = 'inline';
            } else {
                images[index].style.display = 'none';
            }
        }
    }
}

function hideFiveStar() {
    var fiveCheckbox = document.getElementById('FiveStarCheckbox');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        if ("true".localeCompare(images[index].dataset.five) === 0){
            if (fiveCheckbox.checked === true) {
                images[index].style.display = 'inline';
            } else {
                images[index].style.display = 'none';
            }
        }
    }
}

function hideFourStar() {
    var fourCheckbox = document.getElementById('FourStarCheckbox');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        if ("true".localeCompare(images[index].dataset.four) === 0){
            if (fourCheckbox.checked === true) {
                images[index].style.display = 'inline';
            } else {
                images[index].style.display = 'none';
            }
        }
    }
}


function filterone() {

    var armoredCheckbox = document.getElementById('ArmoredCheckbox');
    var flyingCheckbox = document.getElementById('FlyingCheckbox');
    var infantryCheckbox = document.getElementById('InfantryCheckbox');
    var cavalryCheckbox = document.getElementById('CavalryCheckbox');

    var fiveCheckbox = document.getElementById('FiveStarCheckbox');
    var fourCheckbox = document.getElementById('FourStarCheckbox');

    var grailCheckbox = document.getElementById('GrailCheckbox');
    var duoCheckbox = document.getElementById('DuoCheckbox');
    var seasonalCheckbox = document.getElementById('SeasonCheckbox');
    var legendCheckbox = document.getElementById('LegendCheckbox');

    var images = document.getElementsByTagName('img');

    var situation = [grailCheckbox.checked, duoCheckbox.checked, seasonalCheckbox.checked, legendCheckbox.checked];

    for (let index=0; index < images.length; index++) {
        if ("true".localeCompare(images[index].dataset.fix) !== 0) {

            let imgSituation = ["true".localeCompare(images[index].dataset.grail) === 0, "true".localeCompare(images[index].dataset.duo) === 0,
                "true".localeCompare(images[index].dataset.season) === 0, "true".localeCompare(images[index].dataset.legend) === 0];

            let result = [situation[0] && imgSituation[0], situation[1] && imgSituation[1],
                situation[2] && imgSituation[2], situation[3] && imgSituation[3] ];

            let showHide = result[0] || result[1] || result[2] || result[3];

            if (showHide === true) {images[index].style.display = 'inline';}
            else {images[index].style.display = 'none';}
        }
    }
}


function reset() {
    var checkboxes = document.getElementsByTagName('input');
    var images = document.getElementsByTagName('img');

    for (let index=0; index < images.length; index++) {
        images[index].style.display = 'inline';
    }

    for (let index=0; index < checkboxes.length; index++) {
        checkboxes[index].checked = 'true';
    }
}


function textsearch() {
    var images = document.getElementsByTagName('img');
    var text = document.getElementById('searchbar').value;

    for (let index=0; index < images.length; index++) {
        if ("true".localeCompare(images[index].dataset.fix) !== 0) {
            if (!(images[index].alt.toLowerCase().includes(text.toLowerCase()))) {
                images[index].style.display = 'none';
            }
            else images[index].style.display = 'inline';
        }
    }
}