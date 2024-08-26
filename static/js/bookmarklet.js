const siteUrl = 'https://mysite.com:8000/'
const styleUrl = siteUrl + 'static/css/bookmarklet.css'
const minWidth = 250
const minHeight = 250

//load the css
var head = document.getElementsByTagName('head')[0]
var link = document.createElement('link')
link.rel = 'stylesheet'
link.type = 'text/css'
link.href = styleUrl + '?r=' + Math.floor(Math.random() * 9999999999999999)
head.appendChild(link)


//load HTML

var body = document.getElementsByTagName('body')[0]
boxHtml = '<div id="bookmarklet"> <div class="dialog_header"> <h1>Select an image to bookmark: </h1> <a href="#" id="close">&times;</a>  </div>  <div class="images"></div></div>'
body.innerHTML += boxHtml


function bookmarkletLaunch() {
    let bookmarklet = document.getElementById('bookmarklet')
    let imagesFound = bookmarklet.querySelector('.images')

    // clear images found
    imagesFound.innerHTML = ''
//     display bookmarklet
    bookmarklet.style.display = 'block'

//     close event
    bookmarklet.querySelector('#close').addEventListener('click', function () {
        bookmarklet.style.display = 'none'
    })

    let images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]')
    images.forEach(image => {
        if (image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
            var imageFound = document.createElement('img')
            imageFound.src = image.src
            imagesFound.append(imageFound)
        }
    })

//     select image event
    imagesFound.querySelectorAll('img').forEach(image => {
        image.addEventListener('click', function (event) {
            const imageSelected = event.target;
            bookmarklet.style.display = 'none';
            window.open(siteUrl + 'images/create/?url='
                + encodeURIComponent(imageSelected.src)
                + '&title='
                + encodeURIComponent(document.title),
                '_blank'
            );

        })
    })
}

bookmarkletLaunch()