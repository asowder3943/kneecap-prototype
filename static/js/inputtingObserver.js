TimeOutHandler = new Object();

function InputtingObserver(elem, inputCallback, observationDelay) {

    elem.addEventListener('input', () => {
        this.CallbackInterface(elem, inputCallback, observationDelay);
    });
}

function CallbackInterface(elem, firedCallback, DelayFromLast) {
    tmh = TimeOutHandler[elem]
    if (tmh) {
        window.clearTimeout(tmh);
    }
    TimeOutHandler[elem] = window.setTimeout(firedCallback, DelayFromLast);
}
