# Facebook-Messenger-Chatbot
A convenient chatbot for tutor

## Motivation
讓身兼多個家教的老師, 可以利用這個chatbot和學生互動

## API Reference
* Pytransition
* google cloud

## Finitie State Machine
![image](https://github.com/chun2925084/facebook-messenger-bot/blob/master/fsm.png)

## Usage
The initial state is set to user, and the final state is also set to user.

* user
  * Input: "我想問問題"
    * Reply: "ok, 把你的問題傳過來吧!"
  * Input: "我需要大量的題目"
    * Reply: 
      * button:
        * tittle: "需要哪一種類型的呢?"
        * content: "運動學"
        * content: "力學"
  * Input: "幫我把圖片轉成文字!"
    * Reply: "Ok, send it!"
* asking
  * Input: question_image
    * Reply: 
      * button:
        * tittle: "順便標記一下吧!"
        * content: "運動學"
        * content: "力學"
* label
  * Input: "運動學"/"力學"
    * Reply: "等我一下唷!"
* waiting
  * Input :回傳正確答案
    * Reply: "這樣懂了嗎??如果懂得話就回答懂, 不懂就不要裝懂, 直接回答不懂, 我不會生氣~"
* check
  * Input: "懂"
    * Reply: "你怎麼這麼棒!"
  * Input: "不懂"
    * Reply: "那只好下次上課再幫你了" (back to state: user)
* choose:
  * Input: "力學"/"運動學"
    * Reply: 從資料庫抓一張圖片回傳給使用者
    * Reply: 
      * button:
        * tittle: "需要答案嗎?"
        * content: "好!!!"
    * content: "不用~我最厲害!"
* send_question
  * Input: "好!!"/"不用~我最厲害!"
    * Reply: 從資料庫中的對應題目抓出答案給使用者
    * Reply: "這樣懂了嗎??如果懂得話就回答懂, 不懂就不要裝懂, 直接回答不懂, 我不會生氣~"
* ans: 
  * Input: "懂"
    * Reply: "你怎麼這麼棒!"
  * Input: "不懂"
    * Reply: "那只好下次上課再教你了" (back to state: user)
* convert:
  * Input: 使用者送出需要轉換的圖片
    * Reply: server回傳轉換成文字的字串
* produces:
   * Reply: "type finish" (back to state: user)

## Reference
* https://gist.github.com/jczaplew/8307225
