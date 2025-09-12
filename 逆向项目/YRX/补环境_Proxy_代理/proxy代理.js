yuan = {
    "name": "yuan",
    "age": 18,
    "sex": "male"
}

yuan  =  new Proxy(yuan, {
    get: function(target, key) {
        console.log(`getting ${key}!`);
        return target[key];
    },
    set: function(target, key, value) {
        console.log(`setting ${key}!`,target,key,value);
        // target[key] = value;
        // return true;
    return Reflect.set(target, key, value);
    }
});


yuan.age = 18
console.log(yuan.age);
