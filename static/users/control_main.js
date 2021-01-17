const GET_AUTH_URL = "http://0.0.0.0:5002/auth";


function go_to_login_page() {
    window.location.replace(GET_AUTH_URL);
}


const GET_MENU_URL = "http://0.0.0.0:5002/menu_pis"

function go_to_pi_page(id, login) {
    let params = new URLSearchParams({id: id, login: login});
    window.location.replace(GET_MENU_URL + "?" + params.toString());
}


const CREATE_URL = "http://0.0.0.0:5002/v1/create_user/";

function create_user(location) {
    let name = document.getElementById("name").value;
    let surname = document.getElementById("surname").value;
    let last_name = document.getElementById("last_name").value;
    let count_visitors = document.getElementById("count_visitors").value;
    let bluetooth_address_1 = document.getElementById("bluetooth_address_1").value;
    let bluetooth_address_2 = document.getElementById("bluetooth_address_2").value;
    let uuid_device_1 = document.getElementById("uuid_device_1").value;
    let uuid_device_2 = document.getElementById("uuid_device_2").value;

    if (bluetooth_address_1 === bluetooth_address_2) {
        alert("bluetooth_address_1 == bluetooth_address_2 !");
        return;
    }

    if (uuid_device_1 === uuid_device_2) {
        alert("uuid_device_1 == uuid_device_2 !");
        return;
    }

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            // redirect
            alert("Create user with ID " + json.id);
            location.reload();
        }
    };

    xhr.open("POST", CREATE_URL, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify({
        "name": name,
        "surname": surname,
        "last_name": last_name,
        "count_visitors": count_visitors,
        "bluetooth_address_1": bluetooth_address_1,
        "bluetooth_address_2": bluetooth_address_2,
        "uuid_device_1": uuid_device_1,
        "uuid_device_2": uuid_device_2,
        "location": location
    });
    xhr.send(data);
}


const DELETE_URL = "http://0.0.0.0:5002/v1/delete_user_by_id/";

function delete_user(id) {
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            // redirect
            alert("Deleted PI with ID " + json.id);
            location.reload();
        }
    };

    xhr.open("POST", DELETE_URL, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify({
        "id": id
    });
    xhr.send(data);
}


const NULL_CV = "http://0.0.0.0:5002/v1/update_cv_by_fio/";

function update_cv_by_fio(
    id,
    name,
    surname,
    last_name,
    count_visitors,
) {
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            // location.reload();
            document.getElementById(id).innerHTML = "Count Visitors: " + json.count_visitors;
        }
    };

    xhr.open("POST", NULL_CV, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "name": name,
            "surname": surname,
            "last_name": last_name,
            "new_count_visitors": count_visitors
        }
    );
    xhr.send(data);
}


const UPDATE_UUIDS_BY_FIO = "http://0.0.0.0:5002/v1/update_uuids_by_fio/";

function save_changes(
    name,
    surname,
    last_name,
    bluetooth_address_1,
    bluetooth_address_2,
    uuid_device_1,
    uuid_device_2,
    reload= true
) {
    let new_bluetooth_address_1 = document.getElementById(bluetooth_address_1).value;
    let new_bluetooth_address_2 = document.getElementById(bluetooth_address_2).value;
    let new_uuid_device_1 = document.getElementById(uuid_device_1).value;
    let new_uuid_device_2 = document.getElementById(uuid_device_2).value;

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            // update data on PI.
            // reload
            update_cv_by_fio(
                "count_visitors_" + bluetooth_address_1,
                name,
                surname,
                last_name,
                0
            );
            // location.reload();

            if (reload === true) {
                location.reload();
            }
        }
    };

    xhr.open("POST", UPDATE_UUIDS_BY_FIO, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "name": name,
            "surname": surname,
            "last_name": last_name,
            "bluetooth_address_1": new_bluetooth_address_1,
            "bluetooth_address_2": new_bluetooth_address_2,
            "uuid_device_1": new_uuid_device_1,
            "uuid_device_2": new_uuid_device_2
        }
    );
    xhr.send(data);
}


