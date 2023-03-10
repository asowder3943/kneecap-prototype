async function refreshFeed() {
    document.getElementById('feed-refresh-button').classList.add('fa-spin');
    fetch(`refresh`).then(async function () {
        displayFeed()
    })   
}

async function download(video_id, download_type){
    fetch(`download/${video_id}/${download_type}`).then(async function() {
        displayFeedItem(video_id)
    })
}

async function togglePlayed(video_id){
    fetch(`toggle-played/${video_id}`).then(async function() {
        displayFeedItem(video_id)
    })
}

async function toggleHidePlayed(){
    fetch(`toggle-hide-played`).then(async function() {
        displayFeed()
    })
}

async function refreshPlayer(video_id) {
    fetch(`player/${video_id}`).then(async function (response) {
        player.innerHTML = await response.text()
        
    })   
}

async function reverseFeed() {
    fetch(`reverse`).then(async function () {
        displayFeed()
    })   
}

async function displayFeed(){
    fetch(`feed`).then(async function (response) {
        feed.innerHTML = await response.text()
    })
}

async function displayFeedItem(video_id){
    fetch(`feed/${video_id}`).then(async function (response) {
        feedItem = document.getElementById(`feed-item-${video_id}`)
        // feedItem.innerHTML = ""
        feedItem.innerHTML = await response.text()
    })
}