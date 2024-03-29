# 行列のページ

## 概要
行列に関連するライブラリ。
任意の環が乗る行列。  
積と和をそれぞれ定義し、作用させる。  
以下計算量はN×N正方行列のAに対しての物とする。  

|  処理  |  計算量  |
| ---- | ---- |
|  ドット積  |  N^3  |
|  積  |  N^2  |
|  和  |  N^2  |
|  行列累乗(T乗するとき)  |  log(T) * N^3  |

<br></br>

## 用途
累乗部分がデカすぎてメモリが死んじゃう時など  
例えば10^18回移動して到達できる場所はどこ？というときは積を1 if a*b >0 else 0
等にする

<br></br>

## 処理概要
積、和、ドット積は線形代数の教科書を参照してください。

### 累乗 
N×N正方行列AをT乗することを考える。  

1. N×N単位行列Bを作成する。  
2. Tの各bitを下から見る。bit毎に以下を行う.  
2.1. bitが1の時BにBとAのドット積を新たなBとする  
2.2. AとAのドット積を新たなAとする  
3. 最後に出来たBが答え

どうしてこれで出来るんですか？  
ダブリングと一緒  

A^3 * A^2 = A^(3+2)  
のように掛けると冪の部分は足し算として扱われる。  
ここではT乗したいのでいい感じにAを使って表現したい。  
Tを二進数表記して1が経ってるところだけ掛け合わせればA^Tになる。

例)
T = 6  
Tを二進数表記すると110
A^4 * A^2 = A^6
となる

上記アルゴリズムではA^1から始め、A^2, A^4と2進数表記のbitを下から遡っている。  
1になったらかけ合わせてる。


<br></br>


verify
・https://yukicoder.me/problems/no/1340


<br></br>
## NEXT
基底とかも求められるようにしたいよね
