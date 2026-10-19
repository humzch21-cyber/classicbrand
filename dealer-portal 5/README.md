# Classic Brand Dealer Portal — 页面结构说明

## 页面

| 文件 | 左侧菜单 | 内容 |
|---|---|---|
| `index.html` | Overview | 四张指标卡可点选：选中的那张显示底部色条，下方列表随之筛选（Drafts / In production / Ready for pickup / 有发货日期的订单按日期排序），再点一次取消恢复最近 5 条；快捷入口（Kitchen / Vanity / Vanity top / Hardware、三个文档库） |
| `orders.html` | Orders | 订单列表 = 本浏览器里新下的订单 / 保存的草稿（localStorage `cb-dealer-orders`，带 New 标记，排在最前）+ 12 条示例订单；按状态 Tab、产品线、关键字筛选。`?status=draft&highlight=Q-1853` 打开某 Tab 并高亮某条 |
| `order.html` | Orders（详情） | `?id=300010842` 订单详情：标题为 Order #（= SAP SO 号，网站下单以 3 开头的 9 位数），事实条为 Order # · SAP SO / PO #（经销商自填）/ Customer tag / 下单日 / Ready date / 配送，按件逐行的明细（门型颜色、五金配置、Assembly、tag），收货地址与配送方式，右侧金额汇总和状态时间线；草稿可「Continue this quote」回结算页，任何订单可 Reorder（整单放回购物车）或 Print。下单成功后直接跳到这里（`&placed=1` 显示绿色提示） |
| `new-order.html` | New order · 第 1 步 | 先选产品线（Kitchen / Vanity / Vanity top / Hardware，无默认）→ Kitchen / Vanity 选系列卡片；**Vanity top 直接进入第 2 步的台面页**。Vanity 不再弹窗，系列页右上有 Vanity configurator 快捷入口；Hardware 不选系列，直接进入第 2 步的五金列表（同官网 category id 37）；Vanity 系列页和 Vanity 产品页都有「Add a vanity top」快捷入口。`?line=kitchen` / `?line=vanity` 直达，`?line=hardware` 跳到五金列表 |
| `new-order-products.html` | New order · 第 2 步 | 该系列的产品列表：左侧分类树 + 其下方的「Selected」已选小结、Door Style / Colour（浴室柜）或 Door Color + Box Color（厨房）、搜索、SKU 表格（滚动加载，每次 20 行）。厨房和五金配件每行是数量步进器：可以在多个 SKU（含不同 Box）上先设数量，底部购物车条显示「Ready to add · n pieces」，输入**一个** Customer tag 后点 Add to cart，这个 tag 应用到所有暂存的件（批量加 tag）；左上 **Back** 回到第 1 步该产品线；Euroline 有 Door Style（6 种）/ Door Color（全部 Basix + Ultra 色）/ **Door Backing**（仅非平板 shaker 门：White / Grey / Wood grain / Dark Grey）/ Box Color（全部 5 种箱体色）；浴室柜（带腿 / 全板 / Linen / 壁柜）每行是 **Configure** 按钮，弹出配置框（参照官网产品页）：Evolution I / II / III 带腿款需选 Legs（Wood legs 标准 / BL / SV / GD 金属腿）、Knobs（价格册内含的 K02…K08B 为 Included，另有 22 个 Premium 旋钮）+ Knob location、Handles（H02…H09CH-400 Included）+ Handle location、Hardware instruction 必选（Install-Hardware / Install-Back / Loose-Hardware / Loose-Drillholes）、Customer tag、数量，选齐后才能 Add to cart；配置记录在购物车行上（同一 SKU 不同门型/颜色/五金配置是不同的行）。浴室柜 Add to cart 后配置框变为「Added to cart」，带「Add the matching 37″ vanity top」按钮（所有浴室柜系列都有，包括 Fundamentals / Crush；Linen 等非柜体显示「Choose a vanity top」，同样带 tag）：跳到台面页并只显示匹配尺寸（宽 +1″，60″ 按单/双盆 61S/61D，72″ → 73D），Customer tag 自动带过去。行内显示「n in cart · Remove」。结账只能经由「View summary & checkout」抽屉：抽屉按**件**逐行列出，每行填各自的 Customer tag；抽屉里每件右侧有删除按钮，底部 Keep adding 左边有 Clear all（点两次确认，无弹窗）；**必选 Assembly Required Yes/No** 后 Checkout 才可点，选 Yes 时按价格册的 Assembly price 计入总价。`?series=系列id&color=…&door=…` |
| `new-order-vanity-top.html` | New order · 第 2 步（台面） | 按官网 Vanity Top 流程做成一页：上方「1 · Choose a top」按 2 cm Premium Quartz（Pure White / Arctic Glacier / Moonlight / Mist / Whisper / Fusion）、2 cm Regular Quartz（Starlight）、3 cm Premium Quartz（Lava Grey / Moonlight）、Sintered Stone（Carrara Gold · Crush only / Bianco Rumeno）分组，缩略图是价格册实拍小样（`assets/covers/top-*.jpg`）；选完下方「2 · Choose a size」才出现尺寸卡片（9 个洗手台面尺寸，2 cm 石英另有 24/30/36″ 化妆台面，配件：挡水板、侧挡水、水槽）。每张卡片内勾选 Top service（Drill-4 / Drill-8 / CUT-LEFT / CUT-RIGHT）、填 Customer tag、数量、Add to cart；同一 SKU 不同 Top service 组合是购物车里不同的行。勾 CUT-LEFT / CUT-RIGHT 时旁边出现切边尺寸（英寸）必填框，记录为如 `CUT-LEFT 2.5″`。`?size=37&for=SKU&tag=…` 为从浴室柜跳来的匹配模式（顶部提示条，可「Show all sizes」）。工具栏有「Add vanities」快捷入口回到 Vanity 系列页。`?color=AGR` 直达某个台面 |
| `new-order-checkout.html` | New order · 第 3 步 | 只读：Assembly Required、按件逐行的明细（每行含 Customer tag）、收货地址、发货日期、配送方式、Load truck method、汇总（Comment → PO Number 必填）、下单。`?quote=Q-1847` 为编辑草稿 |
| `inventory.html` | Dealer support · Inventory checking | 库存查询索引（对应 classicbrand.ca/cb/stock）。五大类 Kitchen / Vanity / Vanity top / Sintered stone / Hardware，类内按系列或厚度分组，每个按钮是「全称 (缩写)」，点击新标签打开该缩写的库存页（Kitchen SSW → `http://20.151.216.184:39002/KITCHEN-SSW.html`）。不显示任何库存数量 |
| `invoices.html` | My invoices | 应付 / 逾期 / 7 天内到期 / 近 90 天已付 汇总，发票表格（只读，无下载/支付按钮） |
| `price-book.html` | Price book | 按系列的 April 2026 价格册（Crush / Fundamentals / Evolution / Contempo / All-in-One） |
| `catalog.html` / `design-library.html` | Catalog / Design library | 暂时与 Price book 页内容相同，正式清单在 `docs.py` 的 `DOCS` 里替换 |
| `profile.html` | 左下角账户卡片的 Profile 链接 / 顶栏头像 | 账户信息 |
| `support.html` | Dealer support · Customer support | 对应官网 support-retailers-customer-support：CSR 卡片（字段带 `data-sap`）、常见请求、经销商享有的 12 项支持 |
| `support-delivery.html` | Dealer support · Delivery service | 四种 Shipping method、Load truck method、Ready date 流程（官网该页读取失败，内容来自结账页和 170 km 送货范围，需按官网核对） |
| `support-assembly.html` | Dealer support · Assembly service | 10 个工作日完成组装；如何在下单流程里申请（Assembly required: Yes） |
| `support-videos.html` | Dealer support · Assembly videos | 按 Kitchen / Vanity / Doors & hardware 分组的视频卡片；目前每张卡片打开官网 Assembly videos 页，在 `support_pages.py` 的 `VIDEOS` 里给卡片填 YouTube id 即可在 portal 内弹窗播放 |
| `support-replacement.html` | Dealer support · Product replacement | 官网保修政策 + **Request a replacement** 表单（订单号、产品、问题类型、收货日期自动算是否在 7 个工作日内、照片），提交后显示申请号 RR-xxxx 和历史记录（localStorage `cb-dealer-replacements`）。订单详情页有「Report an issue」直接带入订单号 |

所有页面共用 `assets/portal.css`（样式）、`assets/sample-orders.js`（12 条示例订单，含真实 SKU 明细）、`assets/portal.js`（订单读写、弹出提示、移动端菜单）、`assets/catalog.js`（系列、产品目录、购物车）和 `assets/order-summary.js`（View summary 抽屉、左侧 Selected 小结、底部购物车条，产品页和台面页共用）。

## 下单流程的数据

- 系列列表在 `assets/catalog.js` 的 `SERIES`。厨房系列为 Fundamentals / Trends Limited / Trends Select / Econoline / Euroline（卡片图在 `assets/covers/kitchen-*.jpg`）；浴室柜系列为 Evolution III / Evolution II / Evolution I / Crush / Fundamentals（卡片图在 `assets/covers/vanity-*.jpg`；Evolution I 用价格册 NWS 列）。
- 浴室柜 Evolution I / II / III 和 Crush 的 SKU、MSRP、Assembly price 由 `vanity_book.py` 从价格册 PDF 解析生成到 `assets/vanity-book.js`（Evolution I/II/III Price Book June 2026、Crush Price Book March 2026），共 Evolution I 36 / II 70 / III 70 / Crush 13 条，外加通用的拉手旋钮、踢脚板、填充板、层板。价格册换版时：`pdftotext -layout 新.pdf x.txt` 后运行 `python3 vanity_book.py evo.txt crush.txt`。五金选项在 `assets/catalog.js` 的 `hardwareOptions()`（Premium handles 清单待补），门型与颜色在系列项里（Evolution I：NWS / NNO 两列价；Evolution II：Hamilton / Woodstock / Oakville / Venice / Rome / London 六种门型 + 20 个热压膜颜色，Hamilton 平板门另有 PET / Egger 超平板色；Evolution III：Huron / Ontario / Michigan / Erie 四种凹槽门 + 20 色；Crush：NWS / NBS / NGS；Fundamentals：Step Shaker（SSW）/ Bevelled Shaker（BW、MB），SKU 仍用 Quick Reference 的 FUN- 条目）。SKU 保持价格册原样，门型和颜色记录在购物车行上。经销商价 = MSRP × 0.6（`DEALER_MULTIPLIER`，示意值，Assembly price 同样折算）。
- 厨房 SKU = 门板颜色缩写 + 型号（如 `BW-W0930`、`FG-W0930`）。Fundamentals 的颜色在 `SERIES[0].colors`：Bermuda White（BW）、Step Shaker White（SSW）、Fog Grey（FG）、Step Charcoal Grey（SCG）、Narrow White Shaker（NWS）、Narrow Black Shaker（NBS）——BW / FG 为你确认的缩写，其余四个是按同样规则推的，需要时改 `code` 即可。产品页顶部「Door Color」点哪个颜色，SKU 列表就切到哪个前缀（URL 带 `&color=FG`）。
- 30″ 吊柜价格取自官网 Bermuda White 列表（W0930 $242 … W2430 $435，27–36″ 外推），其他柜型按比例换算，不同颜色乘以 `multiplier`。
- **Assembly Required 永远不预选**：每次进入产品页 / 台面页都会清空，必须在 View summary 里点 Yes / No 才能 Checkout；下单确认框里 Assembly 单独一行。
- 浴室台面 MSRP 按价格册台面表的对应列：2 cm Premium Quartz（AGR31-bundle $728 与官网一致）、2 cm Regular Quartz、3 cm Premium Quartz、Sintered Stone 预算档（CAGR）/ 常规档（BIR）；化妆台面 MT24/30/36 与配件价格为示意值。数据在 `assets/catalog.js` 的 `SERIES` 里 id 为 `vanity-top` 的项（`colors` 11 个台面，含 `prefix`、`idx` 价格列、`image`；`services` 四种 Top service）和 `vanityTopProducts()`。
- 结算页按官网 Place Order 结构：收货地址、Shipping ready date、Shipping method（Pick up by dealer – Free / CBC truck stand delivery / Pick up by DC / Pick up by third party）、Load truck method（Load product with skids / Hand carry product with truck，必填）、Customer tag；右侧订单汇总含 HST 13%、**PO Number（必填、高亮）**、Comment、折扣码、Place order / Draft order。
- 购物车存在浏览器 localStorage，跨页面保留；下单成功后清空。顶栏的 Cart 按钮打开 View summary 抽屉（在产品页/台面页原地打开，其他页面跳到最后一条所在的产品页并自动打开抽屉），不再直接进结算页。
- Vanity configurator 是左侧菜单 Workspace 下的独立按钮，新标签打开 https://classicbrand.ca/3d-bathroom-cabinet-configurator/ 。
- 顶栏右侧「Main website / Dealer portal」切换（类似银行不同门户间切换），Main website 回到 https://classicbrand.ca/ ；手机端在菜单顶部为「Back to main website」。
- 订单号：网站下单生成 3 开头的 9 位数字（`assets/portal.js` 的 `nextId`，示例从 300010860 起），即同步到 SAP 的 SO 号；草稿仍是 Q- 开头。订单列表每行显示 Order # 和 PO #。正式规则需与 Ray 确认。
- Hardware 列表在 `assets/catalog.js` 的 `hardwareLineProducts()`：分类同官网 Handle / Knobs / Premium Hardware / Cabinet Light / Drawers and organizers / Hardware and shelf，库存显示 MTO；Handle / Knobs 用价格册的 H / K 代码，Premium Hardware 为 22 个 premium 旋钮（价格待定），Cabinet Light / Drawers and organizers / Hardware and shelf 为示意条目，需换成官网真实清单；Euroline 门背颜色在 Euroline 系列项的 `backing`（`backingOf()`）。
- 图片都在 `assets/covers/`：5 本 April 2026 价格册封面、5 张厨房成品图、5 张浴室柜成品图、11 张台面小样。

## 库存查询索引数据

- 全部在 `assets/inventory.js`：`BASE` 是库存站地址，每个大类有 `pattern`（Kitchen 为已确认的 `KITCHEN-{code}.html`；Vanity / Vanity top / Hardware 的 `VANITY-{code}.html`、`VANITYTOP-{code}.html`、`HARDWARE.html` 是按同样规则推的，若实际 URL 不同改 `pattern`，或给单个条目加 `href`）。
- 全称和系列按 August 2026 Quick Reference Cabinetry Price Book：Fundamentals（SSW / BW / FG / SCG / NWS / NBS / NNO / NSP）、Trends Limited（JV、OW）、Trends Select（MB）、Econoline（E 前缀 + 对应颜色，EFTW / EFTO 对应 Econoline 平板门的 White / Light Oak）、箱体颜色。Vanity 的 MB / SG / LF / RS / SS 和台面颜色（2 cm Premium：PWR / AGR / MLR / MTR / WHR / FUR；2 cm Regular：SLR Starlight；3 cm Premium：LGR Lava Grey、MLR-3CM；Sintered stone：CAG Carrara Gold（Crush only）、BIR Bianco Rumeno）按你给的对照填好。`name` 为空的只剩 CWR 和六个停产色，页面只显示缩写。

## 替换文档

文档文件都放在 `assets/docs/`，文件名与页面里的链接一一对应。
目前只有 `quick-reference-bathroom-price-book-august-2026.pdf` 是真实文件，
其余是一页的占位 PDF（深色底、写着 Placeholder），**同名覆盖即可**，页面无需改动。

发票 PDF 放在 `assets/docs/invoices/INV-xxxxx.pdf`。

## 重新生成页面（可选）

页面由 `build.py` + `pages.py` + `docs.py` 生成，改动侧边栏或文档列表后运行：

```
python3 docs.py    # 为新增文档生成占位 PDF
python3 build.py   # 重新输出全部 HTML
```

不想用 Python 也可以直接改 HTML，页面本身是纯静态文件。

## 2026-10-01 评审修改对照

| # | 意见 | 改动 |
|---|---|---|
| 1 | 返回主网站按钮 | 顶栏 Main website / Dealer portal 切换；手机菜单顶部 Back to main website |
| 2 | Vanity configurator 独立按钮、去掉弹窗 | 左侧 Workspace 下新增 Vanity configurator（外链图标）；Vanity 弹窗删除 |
| 3 | New order 补 Hardware 系列 | 第 1 步新增 Hardware 产品线（Hardware / Premium Hardware），tag、PO 位置不变 |
| 4 | Euroline 页面返回按钮 | 所有第 2 步页面工具栏最左 Back |
| 5 | Euroline 箱体色、门色、门背色 | 全部箱体色和门色；非平板 shaker 门显示 Door Backing 4 选项 |
| 7 | 摘要 Clear all + 单件删除 | 已加 |
| 8 | 恢复批量加 tag | 多 SKU 先设数量，底部一个 tag，一次 Add to cart |
| 9 | 加浴室柜后加匹配台面、复制 tag | Added to cart 面板 → 匹配尺寸台面页，tag 预填 |
| 10 | 台面切边尺寸 | CUT-LEFT / CUT-RIGHT 旁必填英寸 |
| 11 | 显示 SAP SO 号 | Order #（3 开头）= SAP SO，与 PO # 并列显示 |
| 12 | 主网站辅助资料 | Documents 下新增 Videos & guides 页 |

## Dealer support（对应官网 Support for retailers）

左侧菜单新增 Dealer support 一组，六页对应官网六个页面：Customer support、Delivery service、Assembly service、Assembly videos、Product replacement、Inventory checking。每页右上「Same page on classicbrand.ca」打开官网原页；手机端页面顶部有横向切换标签。原 Videos & guides 页已并入 Assembly videos；Profile 移到左下角账户卡片和顶栏头像。页面代码在 `support_pages.py`。

- 第 1 步 Kitchen / Vanity 页、Vanity top 页、Hardware 页顶部是同一组产品线切换（Back + Kitchen / Vanity / Vanity top / Hardware），由 `order_pages.py` 的 `line_bar()` 生成；Hardware 图标为把手。
