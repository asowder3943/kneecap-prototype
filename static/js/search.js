const subscriptions = document.getElementById('subscriptions')
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results')

// run search query whenever search box edit with delay in milliseconds
InputtingObserver(searchInput, searchChannel, 500);

async function searchChannel(e) {
    query = searchInput.value
    fetch(`search/${query}`).then(async function (response) {
        searchResults.innerHTML = await response.text()
    })
}

async function subscribe(id) {
    fetch(`subscribe/${id}`).then(async function () {
        fetch(`subscriptions`).then(async function (response) {
            subscriptions.innerHTML = await response.text()
        })
    })   
}


