'use strict';

class Game {
    constructor( width, height ) {
      this.objs = [];
      this.frame=0;
   
      //もしもwidthやheight何も代入されていなければ、320を代入する
      this.width = width || 320;
      this.height = height || 320;
   
      this.canvas = document.getElementById( 'canvas' );
      //canvasの横幅とたて幅
   
      canvas.width = this.width;
      canvas.height = this.height;
   
      this.ctx = canvas.getContext( '2d' );
    }
   
    //start()を呼び出すことで、メインループが開始される。
    start() {
      this._main();
    }
   
    //メインループ
    _main() {
      //背景を黒く塗りつぶす
      this.ctx.fillStyle = "#fff";
      this.ctx.fillRect( 0, 0, this.width, this.height );
          
      //ゲームに登場するものの数だけ繰り返す
      for (let i=0; i<this.objs.length; i++) {
        //ゲームに登場するもののクラスから、render()を呼び出す
        this.objs[i].render( this.ctx,this.frame );
      }
      this.frame++;
      //_main()を呼び出す（ループさせる）
      requestAnimationFrame(this._main.bind(this));
    }
   
    //ゲームにテキストなどを表示するための関数
    add( obj, x, y ) {
      obj.x = x || 0;
      obj.y = y || 0;
      this.objs.push( obj );
    }
}
   
  //Labelクラス
class Label {
    //Labelの初期設定
    constructor( label ) {
        this._text=[];
        this._displayLength=0;
        this._line=0;
        this.label = label;
        this.font = "16px 'ヒラギノ角ゴ Pro', 'Hiragino Kaku Gothic Pro', 'ＭＳ ゴシック', 'MS Gothic', sans-serif";
        this.color = '#000';
        this.maxLength=30;
        this.baseline = 'top';
        this.interval=0;
    }
   
    //Labelを表示するための関数（メインループから呼び出される）
    render( ctx, frame ) {
        ctx.fillStyle = this.color;
        ctx.font = this.font;
        ctx.textBaseline = this.baseline;
     
        //文字を表示する間隔（はやさ）が0の場合は、文字を一気に表示
        if ( this.interval === 0 ) {
          //表示する文字数を、１行に表示する最大の文字数で割り、切り上げることで、その文字列が何行になるのかが分かる
          this._line = Math.ceil( this.label.length/this.maxLength );
          //文字列の行数だけ繰り返す
          for( var i=0; i<this._line; i++ ) {
            this._text[i] = this._text[i] || '';
            this._text[i] = this.label.substr( i*this.maxLength, this.maxLength );
            //文字列の表示
            ctx.fillText( this._text[i], this.x, this.y + ( i * 25 ) );
          }
        }
        //文字を表示する間隔（はやさ）が0以外の場合、一文字ずつ表示していく
        else {
          if( this._displayLength < this.label.length && frame%this.interval === 0 ) {
            this._text[this._line] = this._text[this._line] || '';
            //this.labelに代入されている文字列を、this._text[this._line]に一文字ずつ入れていく
            this._text[this._line] += this.label.charAt( this._displayLength );
            this._displayLength++;
            if ( this._displayLength % this.maxLength === 0 ) {
              this._line++;
            }
          }
          for( var i=0; i<this._line+1; i++ ) {
            this._text[i] = this._text[i] || '';
            ctx.fillText( this._text[i], this.x, this.y + ( i * 25 ) );
          }
        }
      }
}

var str=document.getElementById( 'str' ).title;
let game=new Game(516,100);
let label=new Label(str);
label.interval=10;
label.maxLength=32;

game.add(label,5,5);
game.start();


