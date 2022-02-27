var request = require('request');
var tenantId = "ID" /*본인의 테넌트 ID */
var order = "stop" /*start or stop*/
var server_name = "null"; /*ex) vc1, vc13, hc5*/
var options = {
    'method': 'POST',
    'url': 'https://api-identity.infrastructure.cloud.toast.com/v2.0/tokens',
    'headers': {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        "auth": {
            "tenantId": tenantId,
            "passwordCredentials": {
                "username": "example@example.com", /* 본인의 클라우드 ID */
                "password": "passwd" /* 비밀번호 */
            }
        }
    })

};
request(options, function (error, response) {
    if (error) 
        throw new Error(error);
    var change = JSON.parse(response.body);
    var token_id = change.access.token.id
    getInstanceList(token_id)
});

function getInstanceList(token_id) {
    var request = require('request');
    var options = {
        'method': 'GET',
        'url': 'https://kr1-api-instance.infrastructure.cloud.toast.com/v2/' + tenantId + '/servers',
        'headers': {
            'X-Auth-Token': token_id
        }
    };
    request(options, function (error, response) {
        if (error) 
            throw new Error(error);
        var change = JSON.parse(response.body);
        if (order == "start") {
            for (var i = 0; i < change.servers.length; i++) {
                var server_id = change.servers[i].id
                var name_id = change.servers[i].name
                /* vc1, vc11, vc13, vc15를 위한 조건문*/
                if (server_name.substring(0, 3) == "vc1") {
                    if (name_id.substr(0, 4) == server_name) {
                        startInstance(token_id, server_id)
                    } else if (name_id.substr(0, 3) == server_name && name_id.substr(0, 4) != "vc11" && name_id.substr(0, 4) != "vc13" && name_id.substr(0, 4) != "vc15") {
                        startInstance(token_id, server_id)
                    }
                } else if (name_id.substr(0, 3) == server_name) {
                    startInstance(token_id, server_id)
                }
            }
        } else if (order == "stop") {
            for (var i = 0; i < change.servers.length; i++) {
                var server_id = change.servers[i].id
                var name_id = change.servers[i].name
                if (server_name.substring(0, 3) == "vc1") {
                    if (name_id.substr(0, 4) == server_name) {
                        stopInstance(token_id, server_id)
                    } else if (name_id.substr(0, 3) == server_name && name_id.substr(0, 4) != "vc11" && name_id.substr(0, 4) != "vc13" && name_id.substr(0, 4) != "vc15") {
                        stopInstance(token_id, server_id)
                    }
                } else if (name_id.substr(0, 3) == server_name) {
                    stopInstance(token_id, server_id)
                }
            }
        }

    });
}

function startInstance(token_id, server_id) {
    var options = {
        'method': 'POST',
        'url': 'https://kr1-api-instance.infrastructure.cloud.toast.com/v2/' + tenantId + '/servers/' + server_id + '/action',
        'headers': {
            'X-Auth-Token': token_id,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"os-start": null})

    };
    request(options, function (error, response) {
        if (error) 
            throw new Error(error);
        }
    );
}

function stopInstance(token_id, server_id) {
    var options = {
        'method': 'POST',
        'url': 'https://kr1-api-instance.infrastructure.cloud.toast.com/v2/' + tenantId + '/servers/' + server_id + '/action',
        'headers': {
            'X-Auth-Token': token_id,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"os-stop": null})

    };
    request(options, function (error, response) {
        if (error) 
            throw new Error(error);
        }
    );
}
