# 互联网软件开发 - 专业术语词典（Java 方向）

> 适用岗位：Java 开发工程师、后端开发、Java 架构师、Spring 全栈
> 适用场景：互联网、金融科技、电商、企业服务
> 整理日期：2026-09-02

---

## 一、核心编程语言与版本

### 1.1 Java 版本演进
- **Java 8 / 11 / 17 / 21 / 25**（LTS 长期支持版本）
- **OpenJDK / Oracle JDK / Amazon Corretto / Alibaba Dragonwell**
- **GraalVM**：新一代多语言虚拟机
- **Kotlin**（Android 首选，与 Java 100% 互操作）
- **Groovy / Scala**（JVM 系语言）

### 1.2 JVM 核心技术
- **JVM 内存模型**：堆 / 栈 / 方法区 / 元空间
- **GC 算法**：G1 / ZGC / Shenandoah / CMS
- **JVM 调优参数**：Xms / Xmx / XX:NewRatio
- **JIT 编译**：C1 / C2
- **字节码 (Bytecode)**
- **类加载机制 / 双亲委派**
- **JMM (Java Memory Model)**：内存可见性

---

## 二、主流框架与中间件

### 2.1 Spring 生态
- **Spring Boot 3.x**：快速开发脚手架
- **Spring Cloud / Spring Cloud Alibaba**：微服务生态
  - Nacos（注册中心 + 配置中心）
  - Sentinel（流量治理）
  - Seata（分布式事务）
  - RocketMQ（消息队列）
- **Spring MVC / Spring WebFlux**
- **Spring Security / Spring Authorization Server**
- **Spring Data JPA / Spring Data Redis**
- **Spring Batch / Spring Integration**
- **Spring AI**（2026 新兴）

### 2.2 ORM 与数据访问
- **MyBatis / MyBatis-Plus**
- **Hibernate / JPA**
- **JdbcTemplate**
- **Druid / HikariCP**：连接池

### 2.3 消息队列
- **Apache RocketMQ**：阿里开源
- **Apache Kafka**：高吞吐日志
- **RabbitMQ**：企业级消息
- **Pulsar**：云原生消息
- **ActiveMQ**：老牌消息

### 2.4 缓存
- **Redis**（主流）
  - 数据结构：String / Hash / List / Set / ZSet
  - 高级特性：Cluster / Sentinel / 持久化
  - 应用：缓存 / 分布式锁 / 限流
- **Caffeine**：本地缓存
- **Memcached**
- **Redisson**：Redis 客户端

### 2.5 数据库
- **关系型**：MySQL / PostgreSQL / Oracle / SQL Server
  - 索引优化 / 慢查询分析
  - 分库分表：Sharding-JDBC / MyCat
  - 主从复制 / 读写分离
- **NoSQL**：MongoDB / Cassandra / HBase
- **图数据库**：Neo4j
- **时序数据库**：InfluxDB / TDengine
- **国产**：OceanBase / TiDB / PolarDB / 达梦

### 2.6 搜索引擎
- **Elasticsearch (ES)**
- **Solr**
- **OpenSearch**

### 2.7 微服务组件
- **服务注册发现**：Eureka / Nacos / Consul / Zookeeper
- **配置中心**：Nacos / Apollo / Spring Cloud Config
- **API 网关**：Spring Cloud Gateway / Kong / Zuul
- **熔断降级**：Sentinel / Hystrix / Resilience4j
- **链路追踪**：SkyWalking / Zipkin / Jaeger
- **分布式事务**：Seata / TCC / Saga
- **分布式锁**：Redisson / Zookeeper

---

## 三、必备技能图谱

### 3.1 后端核心技能
| 类别 | 必备技能 | 出现位置 |
|---|---|---|
| 语言 | Java 17/21、Spring Boot 3.x、Spring Cloud、MyBatis-Plus | 专业技能 |
| 并发 | JVM 调优、多线程、线程池、CompletableFuture、虚拟线程 | 专业技能/项目 |
| 数据 | MySQL 索引优化、Redis、分库分表 | 技能+项目 |
| 中间件 | RocketMQ/RabbitMQ、Kafka、Elasticsearch | 技能+项目 |
| 部署 | Docker、Kubernetes、CI/CD、Nginx | 项目/加分项 |
| 监控 | Prometheus、Grafana、SkyWalking | 项目经验 |

### 3.2 进阶技能
- **性能优化**：JVM 调优、SQL 优化、缓存设计、并发编程
- **高并发**：限流 / 熔断 / 降级 / 缓存 / 异步 / 分布式
- **高可用**：主备 / 集群 / 异地多活 / 容灾
- **微服务架构**：DDD / 中台 / 治理
- **云原生**：Docker / K8s / Istio / Service Mesh
- **DevOps**：CI/CD / 自动化测试 / 监控告警

### 3.3 测试
- **JUnit 5 / TestNG**
- **Mockito / PowerMock**
- **Testcontainers**：集成测试
- **WireMock**：HTTP Mock
- **Gatling / JMeter**：性能测试
- **JaCoCo**：覆盖率
- **SonarQube**：代码质量

### 3.4 构建工具
- **Maven / Gradle**
- **CI/CD**：Jenkins / GitHub Actions / GitLab CI / ArgoCD
- **镜像仓库**：Harbor / DockerHub
- **配置管理**：Nacos / Apollo

---

## 四、典型项目经历模板

### 4.1 应届生项目（无工作经验）
```
1. 仿天猫秒杀系统（2024.03 - 2024.06）
   - 基于 Spring Boot 3.x + Redis 实现商品缓存与限流
   - 使用 RabbitMQ 异步处理订单
   - 压测下单接口 QPS 约 1200，超卖率为 0
   - GitHub: github.com/xxx/seckill

2. 个人博客管理后台（2024.09 - 2024.12）
   - 前后端分离，Spring Boot + Vue 3
   - JWT 鉴权，RBAC 权限模型
   - 上线后约 90 天连续运行无宕机
```

### 4.2 1-3 年经验项目
```
1. 供应链中台重构（2024.06 - 2025.12）
   - 搭建库存/订单/履约三个核心域
   - 完成 MySQL 分库分表（ShardingSphere）
   - 库存查询 TP99 从 1.8s 降至 400ms
   - 支撑日均订单量 60 万+

2. 消息驱动改造（2025.03 - 2025.08）
   - 用 RocketMQ 异步化导入与对账流程
   - 节省 2 台应用服务器资源
   - 消息消费成功率达 99.99%
```

### 4.3 资深项目（5+ 年）
```
1. Spring Cloud Alibaba 微服务架构落地
   - 主导 14 个微服务从单体拆分
   - 部署频率从 6 次/月提升至 210 次/月
   - p95 下单延迟从 1.9s 降至 310ms
   - 引入 SkyWalking 实现全链路追踪
```

---

## 五、高频简历强动词

- 主导 / 负责 / 推进 / 协同 / 落地
- 调研 / 分析 / 优化 / 重构 / 迭代
- 设计 / 选型 / 落地 / 攻坚
- 提升 / 降低 / 节约 / 撬动
- 从 0 到 1 / 体系化 / 闭环 / 沉淀

---

## 六、量化成果模板（Java 方向）

### 6.1 性能优化类
- "**基于 Spring Boot 3.2 和 Spring Cloud Alibaba 完成订单服务重构，接口响应时间从 800ms 降至 350ms**"
- "**压测环境下调整 JVM 堆内存与 GC 策略，2000 并发时 FGC 从 12 次降为 0**"
- "**JVM 调优后，Young GC 平均耗时从 50ms 降至 15ms，系统吞吐量提升 40%**"

### 6.2 业务成果类
- "**促销峰值 QPS 提升至 3000+，系统可用性达 99.95%，年订单量同比提升 18%**"
- "**减少 30% 人工对账成本，获内部季度技术奖**"
- "**库存查询 TP99 从 1.8s 降至 400ms，支撑日均订单量 60 万+**"

### 6.3 架构升级类
- "**将 Spring Boot 单体应用拆分为 14 个微服务，部署频率从 6 次/月提升至 210 次/月**"
- "**使用 RocketMQ 异步化削峰，支撑秒杀场景下 11K events/sec 峰值**"
- "**引入 SkyWalking + ELK 全链路监控，平均故障定位时间从 30 分钟降至 5 分钟**"

---

## 七、常见简历雷区（避免扣分）

❌ **罗列技术栈但没业务场景**：「熟悉 Java、Spring、MySQL」
✅ **改进**：「基于 Spring Boot 3.x 完成订单服务重构，QPS 提升 3 倍」

❌ **只说"负责"不说"做了什么"**：「负责订单模块开发」
✅ **改进**：「设计订单库 10+ 张表并拆分多级缓存，主导订单流程重构」

❌ **没有数字的成果**：「系统运行稳定」
✅ **改进**：「系统可用性 99.95%，年订单量 1000 万+」

❌ **模糊的技术版本**：「精通 Java」
✅ **改进**：「Java 17/21 实际生产经验，熟悉 Spring Boot 3.x 新特性」

❌ **过时的技术栈**：还在写「SSH 框架」「jQuery」
✅ **改进**：突出 Spring Boot 3 / Spring Cloud 2025 / Java 17+ 等 2026 主流技术

---

## 八、参考学习路径

### 8.1 必读书籍
- 《Effective Java》（Joshua Bloch）
- 《深入理解 Java 虚拟机》（周志明）
- 《Java 并发编程实战》
- 《Spring 实战》（Craig Walls）
- 《数据密集型应用系统设计》（DDIA）
- 《凤凰架构》（周志明）

### 8.2 必看官方文档
- Spring 官方文档：spring.io
- MySQL 官方文档
- Redis 官方文档
- RocketMQ / Kafka 官方文档
- Kubernetes 官方文档

### 8.3 优质社区
- **GitHub**：开源项目
- **掘金 / 思否 / CSDN**：技术博客
- **Stack Overflow**：问答
- **美团技术团队 / 阿里云开发者**：大厂博客
- **OSCHINA / V2EX**

### 8.4 认证（加分项）
- **Oracle Java SE 认证**（OCP）
- **Spring Professional Certification**
- **AWS Developer Associate**
- **Kubernetes 管理员认证（CKA）**
- **阿里云 ACA / ACP**
