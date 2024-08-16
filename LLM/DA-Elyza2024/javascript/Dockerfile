# ベースイメージを指定
FROM node

WORKDIR /javascript
COPY da-elyza-rag  da-elyza-rag

# ポート3000番を開放する
EXPOSE 3000

# 
WORKDIR /javascript/da-elyza-rag
CMD ["npm","start"]

