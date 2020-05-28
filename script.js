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


// function called by all checkboxes, using their own data-___ tag as parameter
// not finished, TODO
function filterone(caller_data_tag) {

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

    for (let index=0; index < images.length; index++) {
         if ("true".localeCompare(images[index].dataset.caller_data_tag) === 0){
             if (fourCheckbox.checked === true) {
                 images[index].style.display = 'inline';
             } else {
                 images[index].style.display = 'none';
             }
         }
    }
}


function reset() {
    var checkboxes = document.getElementsByTagName('input');
    var images = document.getElementsByTagName('img');
    var text = document.getElementById('searchbar');


    for (let index=0; index < images.length; index++) {
        images[index].style.display = 'inline';
    }

    for (let index=0; index < checkboxes.length; index++) {
        checkboxes[index].checked = 'true';
    }

    text.value = ""
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



function create(temp) {
    var body = document.getElementsByTagName('body')[0];
    var rows = document.getElementById('myTable').rows;

    var img = document.createElement('img');
    img.src = 'https://www.topolino.it/wp-content/uploads/2019/11/paperinointera_360.png';
    img.height = 50;
    img.width = 50;

    for (let row=0; row < rows.length; row++) {
        if (rows[row].id == temp) {
            var location = rows[row].cells[7];
            console.log(rows[row].cells[7]);
            location.appendChild(img);
        }
    }
}


function readTextFile() {
    var file = 'heroes_data.txt';
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function () {
        if(rawFile.readyState === 4) {
            if(rawFile.status === 200 || rawFile.status == 0) {
                var allText = rawFile.responseText;
                handle_text(allText)
            }
        }
    }
    rawFile.send(null);
}


function handle_text(text) {
    var rows = text.split('\n');
    for (let row=0; row<rows.length; row++) {
        var split_row = rows[row].split(' # ');
        img = createImg(split_row[0], split_row[1], split_row[4], split_row[5].replace(/(\r\n|\n|\r)/gm,""));
        appendImg(img, split_row[2], split_row[3])
        //document.getElementsByTagName('body')[0].appendChild(img);
    }
}


// creates the image tag given parameter and returns it
function createImg(name, src, move_type, attr) {
    var img = document.createElement('img')
    img.alt = name
    img.src = src
    img.height = 40
    img.width = 40
    img.dataset.move = move_type

    if ('data-duo'.localeCompare(attr) == 0) {img.dataset.duo = 'true'}
    if ('data-legend'.localeCompare(attr) == 0) {img.dataset.legend = 'true'}
    if ('data-grail'.localeCompare(attr) == 0) {img.dataset.grail = 'true'}
    if ('data-season'.localeCompare(attr) == 0) {img.dataset.season = 'true'}
    if ('data-five'.localeCompare(attr) == 0) {img.dataset.five = 'true'}
    if ('data-four'.localeCompare(attr) == 0) {img.dataset.four = 'true'}

    return img
}


function appendImg(img, score, wp_col) {
    var rows = document.getElementById('heroes_table').rows;
    var column = parseInt(wp_col,10) + 1;

    for (var row=0; row<rows.length; row++) {
        if (rows[row].id == score) {
        console.log('appending: ' + img.alt)
            rows[row].cells[column].appendChild(img)
        }
    }
}