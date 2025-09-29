flowchart LR
%% ========= ZONES =========
subgraph U[ユーザー/現場UI]
  BROWSER[ブラウザ/社内PC]
  TABLET[タブレット/HMI]
end

subgraph DMZ[DMZ（インターネット境界）]
  WAF[WAF/Reverse Proxy (HTTPS)]
  APIGW[API Gateway]
end

subgraph IT[IT/工場LAN：アプリ&データ]
  LB[(LB)]
  subgraph APCL[APサーバ群（冗長化）]
    AP1[AP#1 (MES/REST API)]
    AP2[AP#2 (MES/REST API)]
  end
  MQ[(Kafka/AMQP)]
  DWH[(Data Lake / DWH)]
  subgraph DBCL[DBサーバ群（クラスタ/レプリカ）]
    DBP[(MES DB: Primary)]
    DBS[(MES DB: Standby)]
  end
  IAM[認証/ID基盤(AD/IdP)]
  SIEM[監視/ログ収集(SIEM)]
  SCHED[最適化/スケジューラ(計画立案)]
  ML[品質分析/異常検知(ML)]
end

subgraph OT[OTゾーン（現場/装置側）]
  LMP[ライン管理PC]
  OPC[OPC-UAサーバ/ゲートウェイ]
  MQTTB[(MQTT Broker OT)]
  PLC1[PLC: SMT/印刷]
  PLC2[PLC: THD/挿入]
  AOI[AOI検査]
  FCT[FCT検査]
  CELL[セルPC/計測器]
  HMI[ライン表示器/HMI]
  AMR1[AMR: 材料搬送]
  AMR2[AMR: 工程間搬送]
end

subgraph EXT[外部業務システム]
  ERP[(ERP/SAP)]
  WMS[(倉庫WMS)]
end

%% ========= FLOWS =========
%% ユーザー→フロント
BROWSER -->|HTTPS| WAF
TABLET -->|HTTPS| WAF
WAF --> APIGW --> LB --> AP1
LB --> AP2

%% AP群 ↔ 認証/監視
AP1 -->|OIDC/SAML| IAM
AP2 -->|OIDC/SAML| IAM
AP1 -.->|Syslog/metrics| SIEM
AP2 -.->|Syslog/metrics| SIEM

%% AP群 ↔ DBクラスタ/DWH
AP1 -->|SQL| DBP
AP2 -->|SQL| DBP
DBP -.->|同期/レプリカ| DBS
AP1 -.->|ETL/日次・時次| DWH
AP2 -.->|ETL/日次・時次| DWH

%% 計画・分析系
AP1 --> SCHED
AP2 --> ML
SCHED -->|計画指示| AP1
ML -->|品質アラート| AP2

%% OTリアルタイム系（収集/制御）
PLC1 -->|OPC-UA| OPC
PLC2 -->|OPC-UA| OPC
AOI -->|OPC-UA| OPC
FCT -->|OPC-UA| OPC
CELL -->|OPC-UA| OPC

OPC -->|Bridge| MQTTB
MQTTB -->|MQTT(リアルタイム)| MQ
MQ -->|ストリーム取込| AP1
MQ -->|ストリーム取込| AP2
AP1 -->|作業指示/段取| LMP
AP2 -->|品質NG停止/通知| LMP
LMP --> HMI

%% AMR動線
AP1 -->|搬送指示| AMR1
AP1 -->|搬送指示| AMR2
AMR1 -->|材料搬送| PLC1
AMR2 -->|工程間搬送| PLC2

%% バッチ連携（外部システム）
AP1 -.->|生産実績/日次| ERP
AP2 -.->|在庫・払出/時次| WMS
ERP -.->|マスタ/受注| AP1
WMS -.->|入出庫実績| AP2

%% ========= STYLES =========
classDef rt stroke:#c00,stroke-width:2px;
classDef batch stroke-dasharray: 4 4,color:#06c,stroke:#06c;
linkStyle 12,13,14,15,16,17,18,19,20,21,22,23 stroke:#c00,stroke-width:2px; %% OT→ITリアルタイム
linkStyle 7,8,10,11,24,25,26,27 stroke:#06c,stroke-dasharray: 4 4;       %% バッチ