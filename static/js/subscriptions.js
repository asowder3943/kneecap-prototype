async function unsubscribe(id) {
    fetch(`unsubscribe/${id}`).then(async function () {
        fetch(`subscriptions`).then(async function (response) {
            subscriptions.innerHTML = await response.text()
        })
    })   
}