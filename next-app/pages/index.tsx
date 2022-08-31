import type { NextPage } from "next";
import Head from "next/head";
import Image from "next/image";
import styles from "../styles/Home.module.css";
import { io, Socket } from "socket.io-client";
import { useEffect, useState } from "react";
import { MQTTConnection } from "../lib/mqtt";
import mqtt from "mqtt";

var socket: Socket;

const Home: NextPage = () => {
  const [mqttClient, setMqttClient] = useState<mqtt.MqttClient>();
  const [mqttPayload, setMqttPayload] = useState("");
  const [wsPayload, setWsPayload] = useState("");

  function socketInitialize() {
    socket = io("http://127.0.0.1:8000/", {
      path: "/ws/socket.io/",
      transports: ["websocket", "polling"],
      reconnection: true,
      reconnectionDelay: 15000,
      reconnectionDelayMax: 300000,
    });

    socket.on("connect", () => {
      console.log("connected");
    });

    socket.on("update-ws", (msg: string) => {
      console.log(msg);
      const payload = JSON.parse(msg);
      setWsPayload(payload["msg"]);
    });
  }

  function mqttInitialize() {
    if (!mqttClient) return;

    mqttClient.on("connect", () => {
      console.log("Connected");
    });
    mqttClient.on("error", (err) => {
      console.error("Connection error: ", err);
    });
    mqttClient.on("reconnect", () => {
      console.warn("Reconnecting");
    });
    mqttClient.on("disconnect", () => {
      console.error("Disconnected");
    });
    mqttClient.on("message", (topic, message) => {
      const payload = { topic, message: JSON.parse(message.toString()) };
      console.log(payload);
      setMqttPayload(payload.message["msg"]);
    });
    mqttClient.subscribe("update-mqtt");
  }

  useEffect(() => {
    socketInitialize();
    setMqttClient(MQTTConnection("127.0.0.1", 8083));
  }, []);

  useEffect(() => {
    mqttInitialize();
  }, [mqttClient]);

  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <div className="sub" style={{ fontSize: 40 }}>
          <p>WebSocket</p>
          <li>{wsPayload}</li>
        </div>
        <div className="sub" style={{ fontSize: 40 }}>
          <p>MQTT</p>
          <li>{mqttPayload}</li>
        </div>
      </main>

      <footer className={styles.footer}>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{" "}
          <span className={styles.logo}>
            <Image src="/vercel.svg" alt="Vercel Logo" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  );
};

export default Home;
