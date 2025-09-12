CrytoJS = require("crypto-js");

function decode(str){
    var CryptoJS = require("crypto-js");
    var KEY = 'aiding6666666666';
    var key = CryptoJS.enc.Utf8.parse(KEY);
    var decrypted = CryptoJS.AES.decrypt(str, key, {
                   // iv: iv,
                   mode: CryptoJS.mode.ECB,
                   padding: CryptoJS.pad.Pkcs7,
    });
    return decrypted.toString(CryptoJS.enc.Utf8)
}
str = '2A4w0jqbUivhDV042Ka+VbfXmH65wRwPgKTNHCnEW2hkVTAx4LzvekaBzGEikZHeZd76cWv47AJyUTbOKe7yEY13bzkzp24hmz4noxbrBM8zKyKA2lsrfwQlHOtc3kTY1vI9fuy+ng0JJWC41PGCkj9a9MzmUnN92cXmfZoJ7JiDAzMBS7XMf/y0XFkzCpf37B4oUP5SQ8AhZe8gmN0V8UIJVQ9+bMWWVMDDsX2izwQFkwfp5Hl99Ougfk6HEWW1L5FZMh2VpjdIRmrMI5y4XbQxDZ1vk9wo1t0nnB0OMd5dgoQUhP4uf8BCM48CjOvGkavZF+ck5aQ476RgksxlUQ=='

console.log(decode(str))