JS逆向知识梳理
====

本内容为一些JS逆向知识的梳理，未来将会添加一些关于逆向案例在其中，也是对自己的知识总结与梳理，大家一起加油！

<br>

1.如何处理无限debbuger?
-------

> 无限debbuger原因：分析网络请求、查看元素的事件监听器、跟踪 js 等需求第一步就要打开浏览器的开发者工具，只要打开开发者工具就可能会碰到无限 debugger 死循环，或者在调试过程中也可能会出现无限 debugger 的死循环。

解决方法：

##### (1）HOOK注入，通过HOOK注入方式实现，替换原方法将原方法的函数变为空；通过HOOK注入方式可以对加密进行断点（诸如cookie内加密）也就是进行跟栈找加密位置，可以通过直接调用如下代码在浏览器调试中进行。

      AAA = Function.prototype.constructor;
      Function.prototype.constructor = function(a)
          {if (a=='debugger'){
          return function(){};
          }
                  return AAA(a);
          };

##### （2）重写关键函数，具体将debugger设置为空函数。重写关键函数可以指定方法名，或者使用 Function.prototype.constructor = function() {} ，这种方法只有在 (function(){}).constructor === Function 时才会生效。
      
      // 重写 eval 案例
       console.log(eval + '')
      // 'function eval() { [native code] }'
      
      // 重写 eval
      window._origin_eval = window.eval
      
      function $eval(src) {
        console.log(
          `==== eveal begin: length=${src.length}, caller=~${$eval.caller && $eval.caller.name} ====`
        )
        console.log(`injected ${document.location}`)
        console.log(src)
        console.log(`==== eval end ====`)
      
        return window._origin_eval(src)
      }
      
      Object.defineProperty(window, 'eval', { value: $eval })
      
      console.log(eval + '')
      // 'function $eval(src) {\n  console.log(\n    `==== eveal begin: length=${src.length}, caller=~${$eval.caller && $eval.caller.name} ====`\n  )\n  console.log(`injected ${document.location}`)\n  console.log(src)\n  console.log(`==== eval end ====`)\n\n  return window._origin_eval(src)\n}'
      
      $eval.toString = function () {
        return 'function eval() { [native code] }'
      }
      
      console.log(eval + '')
      // 'function eval() { [native code] }'

##### （3）断点调试，通过将debugger打上断点，将其设置为False.

[image](https://github.com/zhihuishou/Javascript_Reverse/assets/161868456/b68cfa3b-6a52-4680-8368-fc9866abdbc1)


#### （4） **eval('debugger') 原理，是在虚拟机里面执行debugger的方法**

   ```javascript
   eval("de"+"bu"+"gg"+"er")
   //遇到类似的eval全局变量，可以这样hook
   ```

   ```javascript
   eval = eval; // 1. 保存原始 eval 函数的引用
   eval = function() { // 2. 重写 eval 函数
       if (arguments[0].indexOf('debugger') === -1) // 3. 检查参数中是否包含 "debugger"
           return _eval(arguments[0]); // 4. 不含 debugger 则执行原始 eval
       // 5. 如果包含 debugger，则不执行任何操作（静默跳过）
   }
   
   //*解释：
   //*indexOf('debugger') 检查字符串中是否包含子串 "debugger"。
   ```

   

#### （5） **Function('debugger')() 及其变种 原理跟2类似，只不过是在虚拟机里面执行匿名函数，匿名函数里有debugger的方法**

   

#### （6）**通过函数的方式构建debbuger ，原型链**

   ```javascript
   for (let i=0;i<=5000;i++){
               Function('debugger')()  // 原型链 获取Function
               eval('debugger')
               debugger;
   ```

   

#### （7） **通过添加script标签，插入debugger，直接写入document的body中**

```javascript
        cont = document.body
        var newScript = document.createElement('script');
        newScript.type = 'text/javascript';
        newScript.innerHTML = 'debugger';
        cont.appendChild(newScript);
```


html页面生产时，直接自动生成几千个script标签，标签里只写一个debugger

##### 解决方案：

```
- 使用浏览器插件（如 AutoResponse）拦截或替换响应

- 使用 Never pause here 跳过调试

- 重写相关函数（注意可能破坏业务逻辑）

- 使用 Mapping/Overrides 替换资源

- 自定义浏览器或修改调试器逻辑
```

<br>

2.如何处理webpack打包?
-------

> webpack是一个基于模块化的打包（构建）工具, 它把一切都视作模块，万变不离其中的就是它的自执行函数，只要在逆向中看到类似如下代码，基本可以确定就是webpack函数，从而需要找到如何运行加密模块的自执行函数：类似这个格式 !function('形参'){'加载器'}(['模块'])。

           !function(e) {
          var t = {};
      
          // 加载器  所有的模块都是从这个函数加载 执行
          function n(r) {
              if (t[r])
                  return t[r].exports;
              var o = t[r] = {
                  i: r,
                  l: !1,
                  exports: {}
              };
              return e[r].call(o.exports, o, o.exports, n),
                  o.l = !0,
                  o.exports
          }
      
          n(0)
      }
          ([
              function () {
                  console.log('123456')
              },
      
                    function () {
                  console.log('模块2')
              },
          ])
##### 解决方法：
      扣 + 堆栈看，涉及到webpack，只要扣就完了。实现的方式，找到加密位置进行堆栈查看，找到加载器以及缺失的模块，构造如上的自执行函数，缺什么补什么。



##### 原理：
   Webpack是一个**前端模块打包工具**。它可以将多个模块按照[依赖关系](https://so.csdn.net/so/search?q=依赖关系&spm=1001.2101.3001.7020)进行静态分析，并生成一个或多个打包后的文件。Webpack的主要功能包括：
 ```
   
   1. 模块打包
      将项目中的所有模块（JavaScript、CSS、图片等）当作一个整体，通过依赖关系将它们打包成一个或多个静态资源文件。
   
   2. 依赖管理
      Webpack可以分析模块之间的依赖关系，根据配置的入口文件找出所有依赖的模块，并将其整合到打包结果中。
   
   3. 文件转换
      Webpack本身只能处理JavaScript模块，但通过加载器（Loader）的使用，可以将其他类型的文件（如CSS、LESS、图片等）转换为有效的模块，使其能够被打包到最终的结果中。
   
   4. 代码拆分
      Webpack支持将代码拆分成多个模块，按需加载，实现按需加载和提升应用性能。
   
   5. 插件系统
      Webpack提供了丰富的插件系统，可以通过插件实现各种功能的扩展，例如压缩代码、自动生成HTML文件等。
   ```

<br>

3.如何实现JSPRC调用（RPC，英文 RangPaCong，中文让爬虫，旨在为爬虫开路，秒杀一切，让爬虫畅通无阻！ PS：玩笑话）?
-------

> RPC和抓包工具逻辑是有点类似的（个人理解），都是通过中转站的逻辑将数据包回传，（RPC是通过websocket协议进行）。抓包工具是建立了通信证书的逻辑，从而可以抓到网页数据。而RPC在浏览器中将加密函数暴露出来，在本地直接调用浏览器中对应的加密函数，从而得到加密结果，不必去在意函数具体的执行逻辑，也省去了扣代码、补环境等操作，可以省去大量的逆向调试时间。


       
#### 原理：在网站的控制台新建一个WebScoket客户端链接到服务器通信，调用服务器的接口服务器会发送信息给客户端，客户端接收到要执行的方法执行完js代码后把获得想要的内容发回给服务器，服务器接收到后再显示出来。
       
参考大佬文章可以看这个：    [github:jxhczhl](https://github.com/jxhczhl/JsRpc?tab=readme-ov-file#%E5%AE%9E%E7%8E%B0) 

也可以看这个K哥的文章：     [k哥爬虫](https://baijiahao.baidu.com/s?id=1725536000710059774&wfr=spider&for=pc)

整体内容已经很丰富了，大概过一遍操作逻辑：
> (1)进入调试，将大佬的代码注入snippet

> (2)连接通信，这里就是相当于hook已经构建了一个function你要做的就是怎么让这个RPC连接和你之后要找的加密参数连起来，通过 new Hlclient("ws://127.0.0.1:12080/ws?group=zzz&name=hlg"); 建立一个http协议；

> (3)在你需要获取加密数据的地方打上你的断点，进行代码的调用。构造逻辑作者已经写好了，这里需要注意的是，在你的断点打上后，将构造的函数写入console中。

      demo.regAction("hello3", function (resolve,param) {
                //hello3 是你构建的函数，也就是在之后请求中你需要写进去的。
               // 这里的hlg就是你断点进行加密的函数
                res=hlg(param["user"],param["status"])
                resolve(res);
            })

![image](https://github.com/zhihuishou/Javascript_Reverse/assets/161868456/d8485aed-9a26-45a2-a97e-eab189f66b5c)

> (4)然后就是本地化调用，写最简单的request去请求就完了

<br>

4.hook注入的多种方式，涉及到多种加密方式的直接实现。
-------

>hook注入是JS逆向中，比较流行的，你可以直接在代码调试F12里面的snippets添加代码进行注入，也可以通过油猴脚本的方式，这里分享一个大佬将所有的hook注入方式都写好了，这里我们只需要将其放到我们的snippet代码块上就OK。

>大佬的GITHUB链接： [多种加密方式](https://github.com/Captain0X/hacker_tools/blob/main/crack_encrypt.js)

这里我直接做个案例分析，对某数据网站的加密进行解密，我把大佬的一键注入hook代码放到snippets上，进行运行该脚本。

![image](https://github.com/zhihuishou/Javascript_Reverse/assets/161868456/bcc51e60-993c-4f06-a41d-599dd0c25255)

当我对其他链接进行切换的时候，该hook自动补获了数据，在console里出现了提示，这里分别给到了我们三个值：ENDATA | AES KEY | AES IV | AES加密结果，基本可以判断该加密方式为AES加密，之后的操作就简单了。

![image](https://github.com/zhihuishou/Javascript_Reverse/assets/161868456/425ed3ad-66bc-4a9f-b78f-210f1d175a18)

我们对该返回值的位置右侧function进行断点，不刷新，进行页面切换或者链接的切换，这里就可以断住。然后我们进行堆栈处理，之后就能找到该算法的对应加密信息，虽然他进行代码混淆，但是我们还是能看出来该逻辑就是AES算法的框架。

![image](https://github.com/zhihuishou/Javascript_Reverse/assets/161868456/53d5e378-b846-4b5b-9440-4d58a56c13bd)

<br>

5.javascript的原型链
-------


1. **隐式原型**：所有引用类型（函数、数组、对象）都有 `__proto__` 属性，例如`arr.__proto__`
2. **显式原型**：所有函数拥有`prototype`属性，例如：`func.prototype`
3. **原型对象**：拥有`prototype`属性的对象，在定义函数时被创建

再理解一下`prototype`与`__proto__`

- js中所有的函数都有一个`prototype`的属性，该属性**引用**了一个对象，该对象叫做**原型对象**
- js中每个对象都有一个`__proto__`属性，该属性指向它**构造函数**的`prototype`

##### 那么什么是构造函数呢？

```javascript
function Person() {}
var person = new Person()
```

例如，命名了一个名为Person的函数，第二行代码是根据上面的构造函数定义，那么函数Person可以称之为构造函数的内置对象，例如Array都属于构造函数的一个实例，他们都算实例

**在上面的例子中，person对象是Person构造函数的一个实例，那下面这个例子就可以成立：**

```javascript
person.__proto__ === Person.prototype
```

### 那么原型链到底有什么用？为什么要搞这么复杂？

原型链里的查找机制：基于 `__proto__` 向上搜索原则，例如，`person`实例对象没有`eat`方法，则向上查找`person.__proto__`其构造函数`Person`的`prototype`中查找是否存在`eat`方法，如果存在，则直接调用，否则基于向上查找`Object.prototype`中是否存在`eat`方法，若也不存在，则返回`undefined` 

##### 再举一个例子：

```javascript
const arr = new Array(1,2,3)
arr.reverse()
arr.sort()
//*
//*Array就是一个构造函数，他会有个prototype（Array.prototype)，在这个原型上已经存在了许多方法，那么arr就是我们的构造函数的一个实例
```

<br>

6.定位hooks跟值和混淆与jsvmp
-------

##### 问题：Hooks是万能的吗？Hooks可以被检测到吗？

首先，对方是如何实现反hooks的？例如对eval函数进行修改，网页端可以进行toString检测，如下：

#### （1）.Hook函数检测原理

系统通常通过以下方式检测函数是否被Hook：

- 调用`toString`方法，比较函数的源代码是否被修改。
- 通过原型链上的方法（如`Function.prototype.toString`）获取函数的源代码。

**如下的基于原型链的hook：**

```
javascript
(function(){
console.log(eval.toString());
//备份原 window.eval 函数
var _eval = window.eval;
//直接调用原始函数
_eval("console.log('eval hook');");
//eval 的 hook 函数
window.eval = function(src){
console.log("eval 要执行的代码：",src);
return _eval(src);
}
```

通过toString方法来查看是否和原方法一致

#### （2）. 如何保护Hook函数的方法不被检测？

- 重写`toString`方法，返回原始函数的源代码。
- 修改原型链上的方法，确保返回正确的结果。
- 使用模板字符串动态获取调用者的名字，避免影响其他函数。

##### a.对象属性部分如何hook？

明确什么是对象属性描述符

Object.defineProperty()方法会直接在一个对象上定义一个新属性，或者修改一个对象的现有属性，并返回此对象：

```
javascript
var obj = {}
Object.defineProperty(obj,"x",{value:100})
console.log(Object.getOwnPropertyDescriptor(0bj,"x").value)

```

最常见的hook方案： hook cookie，使用匿名函数进行hook cookie；
```
javascript
(function () {
    'use strict';
    var cookie_cache = document.cookie;
    Object.defineProperty(document, 'cookie', {
        get: function () {
            return cookie_cache;
        },
        set: function (val) {
            console.log('Setting cookie', val);
            // 填写cookie名
            if (val.indexOf('cookie名') != -1) {
                debugger;
            }
            var cookie = val.split(";")[0];
            var ncookie = cookie.split("=");
            var flag = false;
            var cache = cookie_cache.split("; ");
            cache = cache.map(function (a) {
                if (a.split("=")[0] === ncookie[0]) {
                    flag = true;
                    return cookie;
                }
                return a;
            })
            cookie_cache = cache.join("; ");
            if (!flag) {
                cookie_cache += cookie + "; ";
            }
            return cookie_cache;
        }
    });
})();
```

##### b.对象本体的hook

一般情况下会选择使用 ES6的新语法： 代理

  PS：代理是一种非常完善的机制。它几乎无法被检测（不敢说死，但是还没有遇到过检测方案）
       
```
javascript
global = new Proxy(window, { 
get: function(){
console.log(arguments)
}
})
```

**代理是什么？？**

Proxy是[ES6](https://so.csdn.net/so/search?q=ES6&spm=1001.2101.3001.7020)引入的一个强大特性，它允许你创建一个对象的代理，从而可以拦截和自定义该对象的基本操作。Proxy提供了一种机制，可以在对象的基本操作，如属性查找、赋值、枚举、函数调用等之前或之后执行自定义行为。

```javascript
const proxy = new Proxy(target, handler);
```

#### （3）jsvmp虚拟化保护技术


#### （4）特殊跟值技巧：（"经验"才是真正区分逆向高手和逆向菜逼的标尺）

a.看到这类型的数组： [1937774191, 1226093241, 388252375, 3666478592, 2842636476, 372324522, 3817729613, 2969243214]

 b.看到了一个函数名为：hex_md5 => 加密函数

c.该代码也存在加密：

```javascript
o['toString'](d0['enc']['Utf8']);
                                   d0['RC4']['decrypt'](y, d1, {});
                                   d0['enc']['Utf8']['parse'](z)
```

d.看到了axios特征：查找拦截器Jquery 

<br><br>

7.混淆的常见方式
-------
- a.变量名与变量不可视 
- b.控制流平坦化
- c. 花指令
- d.死代码
- e.三目表达式干扰
- f.jsvmp(Virtual Machine based code Protection for JavaScript)


8.实战演练: 猿人学练习题
-------

**1.猿人学第三题（这题真的经典！扣代码+补环境+混淆+内存爆破+console函数改写+正则表达式爆破）：**

出现的绊脚石：

1.函数内存爆破

2.混淆

3.正则表达式的爆破

解决方案：1.优先观察哪些位置被代码无限循环爆破 （肯定存在判断语句） 

2.使用本地替换

##### 解析：

##### 	根据重放攻击，发现第三题的加密逻辑在cookie，通过对比第一次打开网页会在cookie中生成m请求：

![image-20250729205017931](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250729205017931.png)

##### 解析：

##### 	生成m后会重新reload一遍网页，之后就直接加载到正式页面

![image-20250729205136860](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250729205136860.png)

这个逻辑同猿人学第二题有点像，都是属于动态的js cookie端加密，都存在二次显示页面的逻辑，现在我们开始做调试，既然是cookie端，那么先去寻找cookie的函数，看看能不能定位到cookie，首先先通过script的定位进行断点调试，这里我采用的是最笨的方法一步步跟堆栈：

![image-20250729205616211](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250729205616211.png)

既然是cookie也可以选择通过hook定位document的方式：

```javascript
Object.defineProperty(document,"cookie"){
set:function(val){
debugger;
}
return val
}
```

通过hook定位可以直接看到，这里有个很明显的对应关系，document["**"]中间的对应的就是cookie：

![image-20250729211936106](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250729211936106.png)

这里就是进行慢慢补环境和扣代码的情况了，这里有些对应关系需要重新赋值，很多A的键值对并不是正确的，需要在web端点到A函数进去将正确的key复制回来，这里开始扣代码：

![image-20250729212117572](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250729212117572.png)

在这里我犯了一个巨大的错误，就是懒——将所有自执行函数直接一股脑的放入js中了。但也没毛病，只不过这里需要命名全局变量的逻辑跟到自执行函数，有点费劲，不如直接一个个扣：

![image-20250730114256956](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730114256956.png)

这里建议使用本地化替换的方式，这样也好下断点，如果单纯从web页面去断点的话，它每次混淆之后容易短错位置，这里需要注意，这里通过设置debugger进行断点，这里我在document位置也打上了断点：

![image-20250730115848053](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730115848053.png)

在通过简单的进入调试，发现这里出现了一个爆破，setCookie这里的K进入了7593946次循环！这还搞个屁，根据错误点了进去：
![image-20250730120134306](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730120134306.png)

这里还好是因为电脑性能强大，普通电脑不要轻易尝试：

![image-20250730120409970](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730120409970.png)

于是，我这里找到了关于var k的逻辑，这里new了一个新的正则，通过test *** 巴啦啦，让你进去了一个死循环：

![image-20250730120358263](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730120358263.png)

于是我们这里打个断点看看，原因是什么导致的；这里我发现，原因在于这个var j函数，这里var j设置为了false，当if(!j)的时候，就会进入setCookie这个死循环出不来了，随后马上卡死，所以在我们本地化需要将这个j函数命名为**true**;

为什么呢？因为这样就可以进入 i = g['getCookie'](null,"counter"]的逻辑了！之后随着一步步调试这里的函数就过去了。

**这里就是一个代码爆破位置**：

![image-20250730155721818](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730155721818.png)

现在不断地跟栈，再次进入了一个正则表达式的循环逻辑，这里可以看到又进入了一个同上述代码爆破一样的正则的逻辑，这里对h做了一个判断，if***(~g)，这里做了两个步骤，如果~g的话就返回g，否则进入下一个函数：

![image-20250730160126094](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730160126094.png)



**这里是第二个代码爆破位置：**

这里出现了['push'] (Math[“round”] (Math['random'] ()))，为什么会有random？意味着传入了随机数，不断地传递，然后这个**j函数**再次放入这个for循环中！不断去执行函数，这里出现了代码爆破的情况，那么解决方法也很简单；

既然这里针对的是判断(~g)这个逻辑，那么只要让传入的参数等于(~g)这个逻辑就行了，(~g)实际上就是-1，那么让h = -1，这个爆破逻辑就可以解决了！：

![image-20250730160715620](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730160715620.png)

继续持续的跟栈，突然跟到这一段代码后，网页开始进入卡死，网页不会莫名其妙卡死，只有一种可能，内存被爆破了，于是可以在这段代码前打一个debugger，这里出现了一个setInterval，很可疑，这里可以进行一个控制台调用，发现这段代码直接卡死:

”“”**setInterval,A[$b('\x30\x78\x37\x64', '\x4f\x33\x6e\x77') + '\x52\x67'](M), 0x1f4**“”“：
![image-20250730161632285](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730161632285.png)

继续不断单步调试，发现这里的a6又变成了熟悉的正则表达式，并且下面的!a6使用了test方法，从而导致代码再次陷入卡死：
![image-20250730163516628](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730163516628.png)

这里受不了了，直接从原型链设置一个变量改写test方法让其不再进入循环：

```js
RegExp.prototype.test=function(){
return true
}
```

然后就到了需要navigator环境，直接通过获取web端navigator方法：
![image-20250730165202730](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730165202730.png)

![image-20250730165234984](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730165234984.png)

最后，这里console方法在代码里又被改写了，所以需要重新放到代码顶部重写：
![image-20250730165526010](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730165526010.png)

![image-20250730165619281](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730165619281.png)

![image-20250730165538574](C:\Users\110304\AppData\Roaming\Typora\typora-user-images\image-20250730165538574.png)

完美！结束！


