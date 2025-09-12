const p1 = new Promise((resolve,reject) => {
  reject("error")
})
p1.then(res => {
  console.log(res)
}).catch(err => {
    console.log(err)
})
console.log(p1)