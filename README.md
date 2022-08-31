This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

#### Fast-API
```bash
# create virtual environment
python -m venv venv
# active venv
.\venv\scripts\activate
# install required package in requirements.txt
pip install -r requirements.txt
# run 
uvicorn app.main:app
```

#### NextJS

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

#### PostgreSQL

We will trigger NOTIFY function of PostgreSQL to send signal to listener (FastAPI) then FastAPI will publish to broker (MQTT) and emit to WebSocket server as setting.

In this example is listen on topic "update", you can change this as your wish.