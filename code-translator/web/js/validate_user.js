/**
 * Created by olesya on 19-Jun-16.
 */

if (storageAvailable('localStorage')) {
    userName = localStorage.getItem("userName");
    if (userName == null) {
        alert("Only for logged in user");
        document.location.href = "/";
    }
}
else {
    alert("No Local Storage");
}

function storageAvailable(type) {
    try {
        var storage = window[type],
            x = '__storage_test__';
        storage.setItem(x, x);
        storage.removeItem(x);
        return true;
    }
    catch (e) {
        return false;
    }
}