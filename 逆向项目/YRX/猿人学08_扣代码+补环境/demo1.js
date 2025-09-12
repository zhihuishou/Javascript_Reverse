function a(b){
        return (function(){
            return (function(a, b, c){
                function d(){
                    return c + 6000; // 假装返回的是我们需要的关键密文
                }
                function e(){
                }
                console.log(d())
                window.decode = d;
                //
                document.createElement('canvas') // 假装进行样式渲染以及业务代码等不重要内容
            })(100, 1000, 10000)
        })(1, 2, 3)
    }
a()