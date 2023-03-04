<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
 MathJax.Hub.Config({
 tex2jax: {
 inlineMath: [['$', '$'] ],
 displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
 }
 });
</script>

# floor sum query

## 問題

N個の要素を持つ整数列Aが与えられます  
これからM個の整数Qiが渡されるので各Qiについて以下を求めてください  

$ \sum_{1\le j\le N} \lfloor \frac{A_{j}}{Q_{i}} \rfloor  $

## 制約  
$ 1 \leq N \leq 10^5  $  
$ 1 \leq M \leq 10^5  $  
$ 1 \leq A_{j} \leq 10^5$  
$ 1 \leq Q_{i} \leq 10^5$  

<br>

## 想定ルート
<br>

### あるQiについて計算してみます
$A = [1,2,3,4,5,6,7]$  
$Q = [2]$  
<br>
で考えてみます  
本来の計算量では愚直に計算してみても間に合わないのでfloorが同じ値になる箇所をまとめるようにして計算していきます  
そこで、同じ値になるような数値はいくつあるかを見てみると  
$\lfloor \frac{A_{j}}{Q_{i}} \rfloor$が1になる数値は
[1, <font color="Red"><b>2</b>,<b>3</b></font>,4,5,6,7]  
$\lfloor \frac{A_{j}}{Q_{i}} \rfloor$が2になる数値は
[1, 2, 3, <font color="Red"><b>4</b>,<b>5</b></font>,6,7]  
$\lfloor \frac{A_{j}}{Q_{i}} \rfloor$が3になる数値は
[1, 2, 3, 4, 5, <font color="Red"><b>6</b>,<b>7</b></font>]  
になります  
Aが順列(かつソート済み)であれば、
* $\lfloor \frac{A_{j}}{Q_{i}} \rfloor$が同じ値の$A_{j}$の種類数は一部を除き( \* ) $Q_{i}$個存在
* $\lfloor \frac{A_{j}}{Q_{i}} \rfloor$の値をKとしたときK+1の地点は一部を除き( \* )KになるAjの最大値から右に$Q_{i}$個並ぶ  
( \* ) $A_{j}$の値は最大値が決まっていますので$\lfloor \frac{A_{j}}{Q_{i}} \rfloor$が最も大きいものは$Q_{i}$個に満たないことがあります

これらを考えると$\lfloor \frac{A_{j}}{Q_{i}} \rfloor$が初めて1になる地点からQ個区切りでfor文を回して計算していけばよく、各$Q_{i}$で

$計算量は\frac{max(A)}{Q_{i}}$　

程度であることが分かると思います    
一応ちゃんと計算します  
$\lfloor \frac{A_{j}}{Q_{i}} \rfloor * \lfloor \frac{A_{j}}{Q_{i}} \rfloorになる数値の種類数$  
を
をそれぞれ足していくと  
(1 * 2) + (2 * 2) + (3 * 2) = 12  
となり、答えが求められます  
<br>
## 一般のAではどうか
今考えた順列ではなく、$A_{j}$が重複していたり、存在しない値がある場合を考えます  
先程の考察で嬉しかったのはfor文で$Q_{i}$個ずつずらして計算出来ていたところなので、なるべくその性質が残るように変形してみます。
* 重複した値がある場合：その値がAの中に何個あるかを示すような配列Bを作ってみます
* 整数に漏れがある場合(例えば1から5の順列のうち1から4のどれかが無い状態): 上記の配列Bに0個の場合を許すことでよさそうです
<br></br>
 
順列を上記の配列Bにしたので  
順列の時の計算で使った下記がこう変わっているはずです  
【$\lfloor \frac{A_{j}}{Q_{i}} \rfloor * \lfloor \frac{A_{j}}{Q_{i}} \rfloorになる数値の種類数$】  
↓    
【$\lfloor \frac{A_{j}}{Q_{i}} \rfloor * \lfloor \frac{A_{j}}{Q_{i}} \rfloorになる数値の総数$】  
  
<br>

順列の時の考察から$Q_{i}$個並ぶことが分かっているのでBの幅$Q_{i}$の区間和が【$\lfloor \frac{A_{j}}{Q_{i}} \rfloorになる数値の総数$】になります(区間和は累積和やBITなどで適当に取ります)  
順列の嬉しかった性質は変わっておらず、Bの区間和が増えた程度ですがBの区間和は累積和ならO(1)でとれるので無視します  

計算量は
$\frac{max(A)}{Q_{i}}$のまま行けることが分かりました

<br></br>
 次にクエリについて考えます  
 同じ$Q_{i}$は同じ結果になるので何回も計算するのは無駄です  
 なので各$Q_{i}$について計算した値は辞書とかに入れて保存しておき、同じ値が来た時はそこから出力します  
クエリは$1 から 10^5$の値を取りますが全部1つずつくる時が最悪なので  
この時の計算量は  
$\sum_{1 \le i \le 10^5}{\frac{max(A)}{i}} ≒ max(A)*log(max(A))$
になります  
これは十分高速なので解けます