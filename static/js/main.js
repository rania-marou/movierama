const apiUrl = "http://127.0.0.1:8000"

async function fetchAPI(url, method, data) {

    const headers = new Headers();
    headers.append('Content-Type', 'application/json');

    const jwt = getCookie("jwt");
    if (jwt !== null) {
        headers.append('Authorization', 'Bearer ' + jwt);
    }

    const response = await fetch(apiUrl + url, {
        method: method,
        mode: 'cors',
        cache: 'no-cache',
        headers: headers,
        body: data
    });

    if (response.ok && response.status !== 204) {
        return response.json()
    }
    return null;
}

const getParameterByName = (name) => {
    let match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

const parseJwt = (token) => {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
        return null;
    }
};

const setCookie = (name, value, expires, path = '/') => {
    document.cookie = name + '=' + encodeURIComponent(value) + '; expires=' + expires + '; path=' + path
}

const getCookie = (name) => {
    let match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match && match[2] !== "") {
        return match[2];
    }
    return null;
}

const deleteCookie = (name, path) => {
    setCookie(name, '', -1, path)
}
