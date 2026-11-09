"""
Reclass Pro - Painel do Professor (Desktop PyQt6)

Aplicativo desktop integrado ao banco MySQL do Reclass (XAMPP).
Recursos:
  - Visão Geral analítica com cartões KPI e gráficos interativos
  - Gestão de Aulas com barra de ocupação, criação, exclusão e visualização de inscritos
  - Gestão de Agendamentos com alteração de status em 1 clique (Concluir, Cancelar, Agendar)
  - Diretório de Alunos cadastrados com histórico
  - Busca e filtros em tempo real
  - Exportação de dados para CSV (compatível com Excel)
  - Auto-sincronização periódica configurável
  - Conector com o painel web dashP.html (instância única e protocolo reclass://)
"""

import csv
import os
import sys
from datetime import date, datetime, time as dt_time, timedelta

import pymysql
from PyQt6.QtCore import QDate, QRectF, QSize, Qt, QTime, QTimer
from PyQt6.QtGui import QAction, QBrush, QColor, QFont, QIcon, QKeySequence, QPainter, QPainterPath, QPen
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

# ----------------------------------------------------------
# CONFIGURAÇÕES DO BANCO DE DADOS
# ----------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "reclass",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}

# ----------------------------------------------------------
# PALETA DE CORES E IDENTIDADE VISUAL
# ----------------------------------------------------------
AZUL_PRIMARIO = "#1A337A"
AZUL_HOVER = "#24439C"
AZUL_CLARO = "#EEF2FF"
VERDE_SUCESSO = "#10B981"
AMARELO_ALERTA = "#F59E0B"
VERMELHO_PERIGO = "#EF4444"
ROXO_DESTAQUE = "#8B5CF6"
CINZA_FUNDO = "#FFFFFF"
CINZA_BORDA = "#E2E8F0"
TEXTO_ESCURO = "#0F172A"
TEXTO_MUTED = "#64748B"

CORES_GRAFICO = ["#1A337A", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4", "#EC4899"]

ESTILO_GLOBAL = f"""
QMainWindow, QWidget#fundoPrincipal {{
    background-color: {CINZA_FUNDO};
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}}

/* Cabeçalho superior */
QFrame#topoHeader {{
    background-color: #FFFFFF;
    border-bottom: 1px solid {CINZA_BORDA};
    padding: 12px 24px;
}}

QLabel#marcaTitulo {{
    font-size: 20px;
    font-weight: 800;
    color: {AZUL_PRIMARIO};
    letter-spacing: 0.5px;
}}

QLabel#marcaSubtitulo {{
    font-size: 12px;
    color: {TEXTO_MUTED};
    font-weight: 500;
}}

QLabel#statusPill {{
    background-color: #ECFDF5;
    color: #047857;
    border: 1px solid #A7F3D0;
    border-radius: 12px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 600;
}}

/* Cartões KPI */
QFrame#cartaoKpi {{
    background-color: #FFFFFF;
    border-radius: 12px;
    border: 1px solid {CINZA_BORDA};
}}
QFrame#cartaoKpi:hover {{
    border: 1px solid #CBD5E1;
}}

QLabel#kpiTitulo {{
    color: {TEXTO_MUTED};
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

QLabel#kpiValor {{
    color: {TEXTO_ESCURO};
    font-size: 28px;
    font-weight: 800;
}}

QLabel#kpiSubtexto {{
    font-size: 11px;
    color: {TEXTO_MUTED};
}}

/* Caixas dos Gráficos */
QFrame#caixaCard {{
    background-color: #FFFFFF;
    border-radius: 12px;
    border: 1px solid {CINZA_BORDA};
}}

QLabel#caixaTitulo {{
    font-size: 14px;
    font-weight: 700;
    color: {AZUL_PRIMARIO};
}}

/* Abas */
QTabWidget::pane {{
    border: none;
    background: transparent;
}}

QTabBar::tab {{
    background: #E2E8F0;
    color: #475569;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 600;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 6px;
    border: none;
}}

QTabBar::tab:selected {{
    background: #FFFFFF;
    color: {AZUL_PRIMARIO};
    border-bottom: 2px solid {AZUL_PRIMARIO};
}}

QTabBar::tab:hover:!selected {{
    background: #CBD5E1;
    color: {TEXTO_ESCURO};
}}

/* Botões */
QPushButton {{
    background-color: {AZUL_PRIMARIO};
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 12px;
}}
QPushButton:hover {{
    background-color: {AZUL_HOVER};
}}
QPushButton:pressed {{
    background-color: #142557;
}}

QPushButton#btnSucesso {{
    background-color: {VERDE_SUCESSO};
}}
QPushButton#btnSucesso:hover {{
    background-color: #059669;
}}

QPushButton#btnPerigo {{
    background-color: {VERMELHO_PERIGO};
}}
QPushButton#btnPerigo:hover {{
    background-color: #DC2626;
}}

QPushButton#btnSecundario {{
    background-color: #FFFFFF;
    color: #334155;
    border: 1px solid #CBD5E1;
}}
QPushButton#btnSecundario:hover {{
    background-color: #F1F5F9;
    color: {TEXTO_ESCURO};
}}

/* Campos de Busca e Entradas */
QLineEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox {{
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    color: {TEXTO_ESCURO};
}}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus {{
    border: 1.5px solid {AZUL_PRIMARIO};
}}

/* Tabelas */
QTableWidget {{
    background-color: #FFFFFF;
    border: 1px solid {CINZA_BORDA};
    border-radius: 10px;
    gridline-color: #F1F5F9;
    font-size: 12px;
    color: {TEXTO_ESCURO};
    outline: none;
}}

QTableWidget::item {{
    padding: 8px 12px;
    border-bottom: 1px solid #F1F5F9;
}}

QTableWidget::item:selected {{
    background-color: {AZUL_CLARO};
    color: {AZUL_PRIMARIO};
    font-weight: 600;
}}

QHeaderView::section {{
    background-color: #F8FAFC;
    color: {TEXTO_MUTED};
    padding: 10px 12px;
    border: none;
    border-bottom: 2px solid {CINZA_BORDA};
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
}}

/* Barra de Progresso */
QProgressBar {{
    background-color: #E2E8F0;
    border: none;
    border-radius: 6px;
    text-align: center;
    color: #0F172A;
    font-weight: 700;
    font-size: 11px;
    height: 18px;
}}
QProgressBar::chunk {{
    background-color: {AZUL_PRIMARIO};
    border-radius: 6px;
}}

/* Barra de Status */
QStatusBar {{
    background-color: #FFFFFF;
    border-top: 1px solid {CINZA_BORDA};
    color: {TEXTO_MUTED};
    font-size: 11px;
    padding: 4px 10px;
}}

/* Acabamento visual e feedback de interação */
QWidget {{
    background-color: #FFFFFF;
    selection-background-color: {AZUL_CLARO};
    selection-color: {AZUL_PRIMARIO};
}}
QFrame#topoHeader {{
    border-bottom: 1px solid #D9E2F0;
}}
QFrame#cartaoKpi, QFrame#caixaCard {{
    border-radius: 14px;
    background: #FFFFFF;
}}
QFrame#cartaoKpi:hover, QFrame#caixaCard:hover {{
    border-color: #C3D1E7;
}}
QPushButton {{
    min-height: 20px;
    padding: 9px 14px;
}}
QPushButton:disabled {{
    background: #CBD5E1;
    color: #64748B;
}}
QTableWidget {{
    alternate-background-color: #F8FAFC;
    selection-background-color: {AZUL_CLARO};
    selection-color: {AZUL_PRIMARIO};
}}
QTableWidget::item {{
    padding: 9px 10px;
}}
QHeaderView::section {{
    padding-top: 12px;
    padding-bottom: 12px;
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: #F1F5F9;
    width: 10px;
    margin: 2px;
    border-radius: 5px;
}}
QScrollBar::handle:vertical {{
    background: #CBD5E1;
    min-height: 30px;
    border-radius: 5px;
}}
QScrollBar::handle:vertical:hover {{
    background: #94A3B8;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""


# ----------------------------------------------------------
# FUNÇÕES DE BANCO DE DADOS
# ----------------------------------------------------------
def consultar(sql, params=None):
    """Executa SELECT no MySQL e retorna lista de dicionários."""
    conexao = pymysql.connect(**DB_CONFIG)
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()
    finally:
        conexao.close()


def executar(sql, params=None):
    """Executa INSERT, UPDATE, DELETE no MySQL."""
    conexao = pymysql.connect(**DB_CONFIG)
    try:
        with conexao.cursor() as cursor:
            afetados = cursor.execute(sql, params or ())
            return afetados
    finally:
        conexao.close()


def fmt_data(valor):
    if isinstance(valor, (date, datetime)):
        return valor.strftime("%d/%m/%Y")
    return str(valor or "-")


def fmt_hora(valor):
    if isinstance(valor, timedelta):
        total = int(valor.total_seconds())
        return f"{total // 3600:02d}:{(total % 3600) // 60:02d}"
    if isinstance(valor, (datetime, dt_time)):
        return valor.strftime("%H:%M")
    return str(valor or "-")


def converter_data(valor):
    """Normaliza valores DATE/DATETIME do MySQL para comparação com date."""
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    try:
        return date.fromisoformat(str(valor)[:10])
    except (TypeError, ValueError):
        return None


# ----------------------------------------------------------
# WIDGET: GRÁFICO MODERNO DE BARRAS
# ----------------------------------------------------------
class GraficoModerno(QWidget):
    def __init__(self):
        super().__init__()
        self.dados = []
        self.setMinimumHeight(240)

    def definir_dados(self, dados):
        self.dados = dados
        self.update()

    def paintEvent(self, evento):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        largura, altura = self.width(), self.height()

        if not self.dados:
            p.setPen(QColor(TEXTO_MUTED))
            p.setFont(QFont("Segoe UI", 11))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Nenhum dado registrado.")
            p.end()
            return

        margem_esq, margem_dir, margem_topo, margem_base = 35, 20, 30, 45
        area_w = largura - margem_esq - margem_dir
        area_h = altura - margem_topo - margem_base
        maximo = max(valor for _, valor in self.dados) or 1

        # Linhas de grade horizontais sutis
        p.setPen(QPen(QColor("#E2E8F0"), 1, Qt.PenStyle.DashLine))
        for div in [0.25, 0.5, 0.75, 1.0]:
            y_grade = margem_topo + area_h * (1.0 - div)
            p.drawLine(margem_esq, int(y_grade), largura - margem_dir, int(y_grade))
            val_guia = int(maximo * div)
            p.setPen(QColor("#94A3B8"))
            p.setFont(QFont("Segoe UI", 8))
            p.drawText(0, int(y_grade - 7), margem_esq - 6, 14, Qt.AlignmentFlag.AlignRight, str(val_guia))
            p.setPen(QPen(QColor("#E2E8F0"), 1, Qt.PenStyle.DashLine))

        n = len(self.dados)
        espaco = area_w / n
        larg_barra = min(espaco * 0.55, 64)

        for i, (rotulo, valor) in enumerate(self.dados):
            h_barra = (area_h * valor / maximo) if maximo > 0 else 0
            x = margem_esq + i * espaco + (espaco - larg_barra) / 2
            y = margem_topo + area_h - h_barra

            cor = QColor(CORES_GRAFICO[i % len(CORES_GRAFICO)])

            # Desenha a barra com cantos superiores arredondados
            path = QPainterPath()
            path.addRoundedRect(QRectF(x, y, larg_barra, h_barra), 6, 6)
            p.fillPath(path, QBrush(cor))

            # Tag com o valor acima da barra
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(QColor("#0F172A")))
            tag_rect = QRectF(x + (larg_barra - 32) / 2, y - 22, 32, 17)
            tag_path = QPainterPath()
            tag_path.addRoundedRect(tag_rect, 4, 4)
            p.fillPath(tag_path, QBrush(QColor("#1E293B")))

            p.setPen(QColor("#FFFFFF"))
            p.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
            p.drawText(tag_rect, Qt.AlignmentFlag.AlignCenter, str(valor))

            # Rótulo abaixo da barra
            p.setPen(QColor(TEXTO_ESCURO))
            p.setFont(QFont("Segoe UI", 9))
            rotulo_rect = QRectF(margem_esq + i * espaco, altura - margem_base + 8, espaco, 34)
            p.drawText(rotulo_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, rotulo)

        p.end()


# ----------------------------------------------------------
# WIDGET: CARTÃO KPI
# ----------------------------------------------------------
class CartaoKpi(QFrame):
    def __init__(self, titulo, icone="📊", cor_icone="#1A337A", subtexto=""):
        super().__init__()
        self.setObjectName("cartaoKpi")
        self.setMinimumHeight(105)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(18, 14, 18, 14)
        layout_principal.setSpacing(4)

        linha_topo = QHBoxLayout()
        t = QLabel(titulo)
        t.setObjectName("kpiTitulo")

        badge_ico = QLabel(icone)
        badge_ico.setStyleSheet(f"""
            font-size: 16px;
            background-color: {cor_icone}15;
            color: {cor_icone};
            border-radius: 8px;
            padding: 4px 8px;
        """)

        linha_topo.addWidget(t)
        linha_topo.addStretch()
        linha_topo.addWidget(badge_ico)
        layout_principal.addLayout(linha_topo)

        self.lbl_valor = QLabel("-")
        self.lbl_valor.setObjectName("kpiValor")
        layout_principal.addWidget(self.lbl_valor)

        self.lbl_sub = QLabel(subtexto)
        self.lbl_sub.setObjectName("kpiSubtexto")
        layout_principal.addWidget(self.lbl_sub)

    def definir(self, valor, subtexto=None):
        self.lbl_valor.setText(str(valor))
        if subtexto is not None:
            self.lbl_sub.setText(str(subtexto))


# ----------------------------------------------------------
# WIDGET: CAIXA COM GRÁFICO
# ----------------------------------------------------------
class CaixaGrafico(QFrame):
    def __init__(self, titulo, icone="📈"):
        super().__init__()
        self.setObjectName("caixaCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        header = QHBoxLayout()
        ico = QLabel(icone)
        ico.setStyleSheet("font-size: 16px;")
        t = QLabel(titulo)
        t.setObjectName("caixaTitulo")
        header.addWidget(ico)
        header.addWidget(t)
        header.addStretch()
        layout.addLayout(header)

        self.grafico = GraficoModerno()
        layout.addWidget(self.grafico)


# ----------------------------------------------------------
# DIALOG: CRIAR NOVA AULA
# ----------------------------------------------------------
class DialogNovaAula(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastrar Nova Aula de Reposição")
        self.resize(460, 420)
        self.setStyleSheet(ESTILO_GLOBAL)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        tit = QLabel("➕ Nova Aula de Reposição")
        tit.setObjectName("marcaTitulo")
        layout.addWidget(tit)

        form = QFormLayout()
        form.setSpacing(12)

        self.input_titulo = QLineEdit()
        self.input_titulo.setPlaceholderText("Ex: Conversação em Inglês, Reposição Gramática")
        form.addRow("Título da Aula*:", self.input_titulo)

        self.input_data = QDateEdit()
        self.input_data.setCalendarPopup(True)
        self.input_data.setDate(QDate.currentDate())
        form.addRow("Data*:", self.input_data)

        self.input_horario = QTimeEdit()
        self.input_horario.setTime(QTime(19, 0))
        form.addRow("Horário*:", self.input_horario)

        self.input_vagas = QSpinBox()
        self.input_vagas.setRange(1, 150)
        self.input_vagas.setValue(10)
        form.addRow("Vagas Oferecidas*:", self.input_vagas)

        self.input_unidade = QComboBox()
        self.input_unidade.setEditable(True)
        self.input_unidade.addItems(["Unidade Norte", "Unidade Sul", "Unidade Centro", "Unidade Leste", "Online"])
        form.addRow("Unidade*:", self.input_unidade)

        self.input_obs = QTextEdit()
        self.input_obs.setPlaceholderText("Observações ou detalhes da aula (opcional)")
        self.input_obs.setMaximumHeight(80)
        form.addRow("Observações:", self.input_obs)

        layout.addLayout(form)

        # Botões de ação
        botoes = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnSecundario")
        btn_cancelar.clicked.connect(self.reject)

        btn_salvar = QPushButton("Salvar e Publicar Aula")
        btn_salvar.setObjectName("btnSucesso")
        btn_salvar.clicked.connect(self.salvar)

        botoes.addStretch()
        botoes.addWidget(btn_cancelar)
        botoes.addWidget(btn_salvar)
        layout.addLayout(botoes)

    def salvar(self):
        titulo = self.input_titulo.text().strip()
        if not titulo:
            QMessageBox.warning(self, "Campo obrigatório", "Por favor, digite o título da aula.")
            self.input_titulo.setFocus()
            return

        dt = self.input_data.date().toString("yyyy-MM-dd")
        hr = self.input_horario.time().toString("HH:mm:ss")
        vagas = self.input_vagas.value()
        unidade = self.input_unidade.currentText().strip()
        obs = self.input_obs.toPlainText().strip()

        try:
            executar(
                """
                INSERT INTO aulas (titulo, data, horario, vagas, unidade, observacoes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
                (titulo, dt, hr, vagas, unidade, obs),
            )
            QMessageBox.information(self, "Sucesso", "Aula cadastrada com sucesso no banco de dados!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro ao salvar", f"Não foi possível salvar a aula:\n{e}")


# ----------------------------------------------------------
# DIALOG: VER ALUNOS INSCRITOS NA AULA
# ----------------------------------------------------------
class DialogInscritos(QDialog):
    def __init__(self, aula_info, parent=None):
        super().__init__(parent)
        self.aula_info = aula_info
        self.setWindowTitle(f"Inscritos - {aula_info.get('titulo')}")
        self.resize(680, 460)
        self.setStyleSheet(ESTILO_GLOBAL)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Topo
        topo = QHBoxLayout()
        info_txt = QVBoxLayout()
        t = QLabel(f"📚 {aula_info.get('titulo')}")
        t.setObjectName("marcaTitulo")
        st = QLabel(f"Data: {fmt_data(aula_info.get('data'))} às {fmt_hora(aula_info.get('horario'))} | Unidade: {aula_info.get('unidade')}")
        st.setObjectName("marcaSubtitulo")
        info_txt.addWidget(t)
        info_txt.addWidget(st)
        topo.addLayout(info_txt)
        topo.addStretch()

        self.lbl_vagas = QLabel()
        self.lbl_vagas.setObjectName("statusPill")
        topo.addWidget(self.lbl_vagas)
        layout.addLayout(topo)

        # Tabela de alunos inscritos
        self.tabela = QTableWidget(0, 4)
        self.tabela.setHorizontalHeaderLabels(["ID Agendamento", "Nome do Aluno", "E-mail", "Status"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabela.verticalHeader().setVisible(False)
        layout.addWidget(self.tabela)

        # Ações
        acoes = QHBoxLayout()
        btn_concluir = QPushButton("✅ Concluir Selecionado")
        btn_concluir.setObjectName("btnSucesso")
        btn_concluir.clicked.connect(lambda: self.alterar_status_selecionado("concluida"))

        btn_cancelar_agend = QPushButton("❌ Cancelar Selecionado")
        btn_cancelar_agend.setObjectName("btnPerigo")
        btn_cancelar_agend.clicked.connect(lambda: self.alterar_status_selecionado("cancelada"))

        btn_fechar = QPushButton("Fechar")
        btn_fechar.setObjectName("btnSecundario")
        btn_fechar.clicked.connect(self.accept)

        acoes.addWidget(btn_concluir)
        acoes.addWidget(btn_cancelar_agend)
        acoes.addStretch()
        acoes.addWidget(btn_fechar)
        layout.addLayout(acoes)

        self.carregar_inscritos()

    def carregar_inscritos(self):
        try:
            sql = """
                SELECT g.id AS agend_id, g.status, u.nome, u.email
                FROM agendamentos g
                LEFT JOIN usuarios u ON u.id = g.id_aluno
                WHERE g.aula = %s AND g.data = %s AND g.horario = %s
                ORDER BY g.id DESC
            """
            inscritos = consultar(sql, (self.aula_info["titulo"], self.aula_info["data"], self.aula_info["horario"]))

            self.tabela.setRowCount(len(inscritos))
            ocupadas = sum(1 for i in inscritos if i["status"] != "cancelada")
            vagas = self.aula_info.get("vagas") or 0
            self.lbl_vagas.setText(f"Ocupação: {ocupadas} / {vagas} vagas")

            for row, item in enumerate(inscritos):
                item_id = QTableWidgetItem(str(item["agend_id"]))
                item_nome = QTableWidgetItem(str(item["nome"] or "(Aluno sem nome)"))
                item_email = QTableWidgetItem(str(item["email"] or "-"))

                st_nome = item["status"] or "agendada"
                badge = QLabel(st_nome.capitalize())
                badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
                if st_nome == "concluida":
                    badge.setStyleSheet("background: #ECFDF5; color: #047857; font-weight: 700; border-radius: 4px; padding: 4px;")
                elif st_nome == "cancelada":
                    badge.setStyleSheet("background: #FEF2F2; color: #B91C1C; font-weight: 700; border-radius: 4px; padding: 4px;")
                else:
                    badge.setStyleSheet("background: #FEF3C7; color: #B45309; font-weight: 700; border-radius: 4px; padding: 4px;")

                self.tabela.setItem(row, 0, item_id)
                self.tabela.setItem(row, 1, item_nome)
                self.tabela.setItem(row, 2, item_email)
                self.tabela.setCellWidget(row, 3, badge)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao consultar inscritos: {e}")

    def alterar_status_selecionado(self, novo_status):
        row = self.tabela.currentRow()
        if row < 0:
            QMessageBox.information(self, "Aviso", "Selecione um aluno na lista para alterar o status.")
            return

        agend_id = self.tabela.item(row, 0).text()
        try:
            executar("UPDATE agendamentos SET status = %s WHERE id = %s", (novo_status, agend_id))
            self.carregar_inscritos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao atualizar status: {e}")


# ----------------------------------------------------------
# DIALOG: PERFIL E HISTÓRICO DO ALUNO
# ----------------------------------------------------------
class DialogDetalheAluno(QDialog):
    """Exibe um resumo do aluno e seu histórico de agendamentos."""
    def __init__(self, aluno, parent=None):
        super().__init__(parent)
        self.aluno = aluno
        self.setWindowTitle(f"Perfil do aluno - {aluno.get('nome') or 'Aluno'}")
        self.resize(780, 520)
        self.setStyleSheet(ESTILO_GLOBAL)

        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(22, 22, 22, 22)
        raiz.setSpacing(14)

        topo = QHBoxLayout()
        bloco = QVBoxLayout()
        nome = QLabel(str(aluno.get("nome") or "Aluno sem nome"))
        nome.setObjectName("marcaTitulo")
        email = QLabel(str(aluno.get("email") or "E-mail não informado"))
        email.setObjectName("marcaSubtitulo")
        bloco.addWidget(nome)
        bloco.addWidget(email)
        topo.addLayout(bloco)
        topo.addStretch()
        self.lbl_resumo = QLabel("Carregando histórico...")
        self.lbl_resumo.setObjectName("statusPill")
        topo.addWidget(self.lbl_resumo)
        raiz.addLayout(topo)

        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setStyleSheet(f"color: {CINZA_BORDA};")
        raiz.addWidget(separador)

        titulo_hist = QLabel("Histórico de aulas")
        titulo_hist.setObjectName("caixaTitulo")
        raiz.addWidget(titulo_hist)

        self.tabela = QTableWidget(0, 5)
        self.tabela.setHorizontalHeaderLabels(["ID", "Aula", "Data", "Horário", "Status"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.verticalHeader().setVisible(False)
        raiz.addWidget(self.tabela, 1)

        rodape = QHBoxLayout()
        rodape.addStretch()
        fechar = QPushButton("Fechar")
        fechar.setObjectName("btnSecundario")
        fechar.clicked.connect(self.accept)
        rodape.addWidget(fechar)
        raiz.addLayout(rodape)
        self.carregar_historico()

    def carregar_historico(self):
        try:
            historico = consultar(
                """SELECT id, aula, data, horario, status FROM agendamentos
                   WHERE id_aluno = %s ORDER BY data DESC, horario DESC, id DESC LIMIT 200""",
                (self.aluno["id"],),
            )
            concluidas = sum(1 for item in historico if (item.get("status") or "agendada") == "concluida")
            pendentes = sum(1 for item in historico if (item.get("status") or "agendada") == "agendada")
            self.lbl_resumo.setText(f"{len(historico)} registros · {concluidas} concluídas · {pendentes} agendadas")
            self.tabela.setRowCount(len(historico))
            for row, item in enumerate(historico):
                valores = [item.get("id"), item.get("aula"), fmt_data(item.get("data")), fmt_hora(item.get("horario")), (item.get("status") or "agendada").capitalize()]
                for col, valor in enumerate(valores):
                    cell = QTableWidgetItem(str(valor if valor is not None else "-"))
                    cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.tabela.setItem(row, col, cell)
        except Exception as erro:
            QMessageBox.critical(self, "Erro ao carregar histórico", f"Não foi possível consultar o histórico do aluno:\n{erro}")


# ----------------------------------------------------------
# JANELA PRINCIPAL
# ----------------------------------------------------------
class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reclass Pro | Gestão de Aulas")
        self.resize(1180, 760)
        self.setMinimumSize(950, 620)
        self.setStyleSheet(ESTILO_GLOBAL)

        # Cache de dados em memória para filtros rápidos
        self.cache_aulas = []
        self.cache_agendamentos = []
        self.cache_alunos = []

        # Widget central
        fundo = QWidget()
        fundo.setObjectName("fundoPrincipal")
        self.setCentralWidget(fundo)

        layout_principal = QVBoxLayout(fundo)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # 1. Topo Header
        topo = self._criar_cabecalho()
        layout_principal.addWidget(topo)

        # 2. Área com Abas
        area_conteudo = QWidget()
        layout_conteudo = QVBoxLayout(area_conteudo)
        layout_conteudo.setContentsMargins(24, 16, 24, 16)
        layout_conteudo.setSpacing(14)

        self.abas = QTabWidget()
        layout_conteudo.addWidget(self.abas)
        layout_principal.addWidget(area_conteudo, 1)

        # Criar as abas
        self._criar_aba_visao_geral()
        self._criar_aba_aulas()
        self._criar_aba_agendamentos()
        self._criar_aba_alunos()

        # 3. Barra de Status
        self.barra_status = QStatusBar()
        self.setStatusBar(self.barra_status)
        self.barra_status.showMessage("Pronto. Ctrl+R atualiza · Ctrl+N cria uma aula · Ctrl+E exporta a aba atual.")

        # Atalhos de teclado para as ações frequentes
        acao_atualizar = QAction("Atualizar dados", self)
        acao_atualizar.setShortcut(QKeySequence("Ctrl+R"))
        acao_atualizar.triggered.connect(self.carregar_dados)
        self.addAction(acao_atualizar)
        acao_nova_aula = QAction("Nova aula", self)
        acao_nova_aula.setShortcut(QKeySequence("Ctrl+N"))
        acao_nova_aula.triggered.connect(self.abrir_dialog_nova_aula)
        self.addAction(acao_nova_aula)
        acao_exportar = QAction("Exportar aba atual", self)
        acao_exportar.setShortcut(QKeySequence("Ctrl+E"))
        acao_exportar.triggered.connect(self.exportar_tabela_ativa)
        self.addAction(acao_exportar)

        # 4. Timer de Auto-Refresh
        # Criar o timer depois da barra de status e iniciar apos a criacao.
        self.timer_refresh = QTimer(self)
        self.timer_refresh.timeout.connect(self.carregar_dados)
        self.timer_refresh.start(30000)

        # Carregar dados iniciais
        self.carregar_dados()

    # ------------------------------------------------------
    # CABEÇALHO SUPERIOR
    # ------------------------------------------------------
    def _criar_cabecalho(self):
        topo = QFrame()
        topo.setObjectName("topoHeader")
        layout = QHBoxLayout(topo)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(16)

        # Logo / Títulos
        info = QVBoxLayout()
        tit = QLabel("RECLASS PRO")
        tit.setObjectName("marcaTitulo")
        sub = QLabel("Gestão acadêmica · Painel do Professor · MySQL")
        sub.setObjectName("marcaSubtitulo")
        info.addWidget(tit)
        info.addWidget(sub)
        layout.addLayout(info)

        # Status Pill
        self.status_pill = QLabel("● Conectando ao MySQL...")
        self.status_pill.setObjectName("statusPill")
        layout.addWidget(self.status_pill)

        layout.addStretch()

        # Controle de Auto-refresh
        lbl_auto = QLabel("Atualização:")
        lbl_auto.setStyleSheet(f"color: {TEXTO_MUTED}; font-size: 11px; font-weight: 600;")
        layout.addWidget(lbl_auto)

        self.combo_auto = QComboBox()
        self.combo_auto.addItems(["Manual", "Auto 15s", "Auto 30s", "Auto 60s"])
        self.combo_auto.setCurrentIndex(2)  # default 30s
        self.combo_auto.currentIndexChanged.connect(self._configurar_timer_auto)
        layout.addWidget(self.combo_auto)

        # Botão Nova Aula
        btn_nova_aula = QPushButton("➕ Nova Aula")
        btn_nova_aula.setObjectName("btnSucesso")
        btn_nova_aula.clicked.connect(self.abrir_dialog_nova_aula)
        layout.addWidget(btn_nova_aula)

        # Botão Atualizar
        self.btn_refresh = QPushButton("↻ Atualizar")
        self.btn_refresh.clicked.connect(self.carregar_dados)
        layout.addWidget(self.btn_refresh)

        # O timer e iniciado em __init__, depois de ser criado.
        # Nao iniciar aqui: o cabecalho e montado antes da criacao do QTimer.
        return topo

    def _configurar_timer_auto(self, index):
        tempos = [0, 15000, 30000, 60000]
        ms = tempos[index]
        if ms == 0:
            self.timer_refresh.stop()
            self.barra_status.showMessage("Atualização automática pausada.")
        else:
            self.timer_refresh.start(ms)
            self.barra_status.showMessage(f"Atualização automática a cada {ms // 1000} segundos.")

    # ------------------------------------------------------
    # ABA 1: VISÃO GERAL
    # ------------------------------------------------------
    def _criar_aba_visao_geral(self):
        aba = QWidget()
        outer = QVBoxLayout(aba)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        conteudo = QWidget()
        layout = QVBoxLayout(conteudo)
        layout.setContentsMargins(4, 10, 10, 18)
        layout.setSpacing(18)

        # Cabeçalho contextual do dashboard
        cabecalho = QHBoxLayout()
        titulos = QVBoxLayout()
        tit = QLabel("Visão geral da operação")
        tit.setStyleSheet(f"font-size: 21px; font-weight: 800; color: {TEXTO_ESCURO};")
        self.lbl_sub_dashboard = QLabel(datetime.now().strftime("Resumo atualizado em %d/%m/%Y"))
        self.lbl_sub_dashboard.setStyleSheet(f"font-size: 12px; color: {TEXTO_MUTED};")
        titulos.addWidget(tit)
        titulos.addWidget(self.lbl_sub_dashboard)
        cabecalho.addLayout(titulos)
        cabecalho.addStretch()
        lbl_atalhos = QLabel("Dica: Ctrl+R atualiza · Ctrl+N cria aula · Ctrl+E exporta")
        lbl_atalhos.setStyleSheet(f"color: {TEXTO_MUTED}; font-size: 11px; background: #FFFFFF; border: 1px solid {CINZA_BORDA}; border-radius: 8px; padding: 8px 10px;")
        cabecalho.addWidget(lbl_atalhos)
        layout.addLayout(cabecalho)

        # Indicadores principais
        grade = QGridLayout()
        grade.setSpacing(14)
        self.kpi_aulas = CartaoKpi("Aulas cadastradas", "📚", AZUL_PRIMARIO, "Total no sistema")
        self.kpi_agend = CartaoKpi("Agendamentos", "📝", AMARELO_ALERTA, "Todos os status")
        self.kpi_ocup = CartaoKpi("Ocupação média", "📈", VERDE_SUCESSO, "Percentual de vagas")
        self.kpi_vagas = CartaoKpi("Vagas oferecidas", "🪑", ROXO_DESTAQUE, "Capacidade máxima")
        self.kpi_vazias = CartaoKpi("Aulas sem alunos", "⚠️", VERMELHO_PERIGO, "Precisam de divulgação")
        self.kpi_alunos = CartaoKpi("Alunos cadastrados", "👥", "#06B6D4", "Estudantes ativos")
        for i, card in enumerate([self.kpi_aulas, self.kpi_agend, self.kpi_ocup, self.kpi_vagas, self.kpi_vazias, self.kpi_alunos]):
            grade.addWidget(card, i // 3, i % 3)
        layout.addLayout(grade)

        # Gráficos em uma grade, mais legíveis em telas menores
        grade_graficos = QGridLayout()
        grade_graficos.setSpacing(14)
        self.g_status = CaixaGrafico("Agendamentos por status", "📊")
        self.g_unidade = CaixaGrafico("Ocupação por unidade", "🏢")
        self.g_mes = CaixaGrafico("Evolução mensal de agendamentos", "📅")
        self.g_status.grafico.setMinimumHeight(220)
        self.g_unidade.grafico.setMinimumHeight(220)
        self.g_mes.grafico.setMinimumHeight(210)
        grade_graficos.addWidget(self.g_status, 0, 0)
        grade_graficos.addWidget(self.g_unidade, 0, 1)
        grade_graficos.addWidget(self.g_mes, 1, 0, 1, 2)
        layout.addLayout(grade_graficos)

        # Agenda próxima + painel de atenção
        linha_inferior = QHBoxLayout()
        linha_inferior.setSpacing(14)

        caixa_agenda = QFrame()
        caixa_agenda.setObjectName("caixaCard")
        caixa_agenda_layout = QVBoxLayout(caixa_agenda)
        caixa_agenda_layout.setContentsMargins(18, 16, 18, 16)
        caixa_agenda_layout.setSpacing(10)
        tit_agenda = QLabel("Próximas aulas")
        tit_agenda.setObjectName("caixaTitulo")
        subt_agenda = QLabel("Aulas de hoje e dos próximos dias")
        subt_agenda.setStyleSheet(f"font-size: 11px; color: {TEXTO_MUTED};")
        caixa_agenda_layout.addWidget(tit_agenda)
        caixa_agenda_layout.addWidget(subt_agenda)
        self.t_proximas = QTableWidget(0, 4)
        self.t_proximas.setHorizontalHeaderLabels(["Data", "Hora", "Aula", "Vagas"])
        self.t_proximas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.t_proximas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.t_proximas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.t_proximas.setAlternatingRowColors(True)
        self.t_proximas.verticalHeader().setVisible(False)
        self.t_proximas.setMinimumHeight(190)
        caixa_agenda_layout.addWidget(self.t_proximas)
        linha_inferior.addWidget(caixa_agenda, 3)

        caixa_alertas = QFrame()
        caixa_alertas.setObjectName("caixaCard")
        caixa_alertas_layout = QVBoxLayout(caixa_alertas)
        caixa_alertas_layout.setContentsMargins(18, 16, 18, 16)
        caixa_alertas_layout.setSpacing(10)
        tit_alertas = QLabel("Pontos de atenção")
        tit_alertas.setObjectName("caixaTitulo")
        desc_alertas = QLabel("Sugestões baseadas nos dados atuais")
        desc_alertas.setStyleSheet(f"font-size: 11px; color: {TEXTO_MUTED};")
        caixa_alertas_layout.addWidget(tit_alertas)
        caixa_alertas_layout.addWidget(desc_alertas)
        self.lbl_alertas = QLabel("Os alertas aparecerão após a primeira sincronização.")
        self.lbl_alertas.setWordWrap(True)
        self.lbl_alertas.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.lbl_alertas.setStyleSheet(f"background: #F8FAFC; color: {TEXTO_ESCURO}; border: 1px solid {CINZA_BORDA}; border-radius: 10px; padding: 14px; font-size: 12px; line-height: 1.5;")
        caixa_alertas_layout.addWidget(self.lbl_alertas, 1)
        linha_inferior.addWidget(caixa_alertas, 2)

        layout.addLayout(linha_inferior)
        layout.addStretch(1)
        scroll.setWidget(conteudo)
        outer.addWidget(scroll)
        self.abas.addTab(aba, "📊 Visão Geral")

    # ------------------------------------------------------
    # ABA 2: AULAS
    # ------------------------------------------------------
    def _criar_aba_aulas(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(12)

        # Barra de ferramentas
        barra = QHBoxLayout()
        barra.setSpacing(10)

        self.filtro_aula_busca = QLineEdit()
        self.filtro_aula_busca.setPlaceholderText("🔍 Filtrar por título da aula...")
        self.filtro_aula_busca.textChanged.connect(self._aplicar_filtro_aulas)
        barra.addWidget(self.filtro_aula_busca, 2)

        self.filtro_aula_unidade = QComboBox()
        self.filtro_aula_unidade.addItem("Todas as Unidades")
        self.filtro_aula_unidade.currentIndexChanged.connect(self._aplicar_filtro_aulas)
        barra.addWidget(self.filtro_aula_unidade, 1)

        btn_ver_inscritos = QPushButton("👥 Ver Inscritos")
        btn_ver_inscritos.setObjectName("btnSecundario")
        btn_ver_inscritos.clicked.connect(self.abrir_inscritos_selecionado)
        barra.addWidget(btn_ver_inscritos)

        btn_nova = QPushButton("➕ Nova Aula")
        btn_nova.setObjectName("btnSucesso")
        btn_nova.clicked.connect(self.abrir_dialog_nova_aula)
        barra.addWidget(btn_nova)

        btn_excluir = QPushButton("🗑️ Excluir Aula")
        btn_excluir.setObjectName("btnPerigo")
        btn_excluir.clicked.connect(self.excluir_aula_selecionada)
        barra.addWidget(btn_excluir)

        btn_csv = QPushButton("📥 Exportar CSV")
        btn_csv.setObjectName("btnSecundario")
        btn_csv.clicked.connect(lambda: self.exportar_tabela_csv(self.t_aulas, "aulas_reclass.csv"))
        barra.addWidget(btn_csv)

        layout.addLayout(barra)

        # Tabela
        colunas = ["ID", "Título da Aula", "Data", "Horário", "Unidade", "Vagas", "Ocupação"]
        self.t_aulas = QTableWidget(0, len(colunas))
        self.t_aulas.setHorizontalHeaderLabels(colunas)
        self.t_aulas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.t_aulas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.t_aulas.setAlternatingRowColors(True)
        self.t_aulas.verticalHeader().setVisible(False)
        self.t_aulas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.t_aulas.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.t_aulas.doubleClicked.connect(self.abrir_inscritos_selecionado)

        layout.addWidget(self.t_aulas)
        self.abas.addTab(aba, "📚 Gestão de Aulas")

    # ------------------------------------------------------
    # ABA 3: AGENDAMENTOS
    # ------------------------------------------------------
    def _criar_aba_agendamentos(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(12)

        # Barra de ferramentas
        barra = QHBoxLayout()
        barra.setSpacing(10)

        self.filtro_agend_busca = QLineEdit()
        self.filtro_agend_busca.setPlaceholderText("🔍 Filtrar por aluno ou aula...")
        self.filtro_agend_busca.textChanged.connect(self._aplicar_filtro_agendamentos)
        barra.addWidget(self.filtro_agend_busca, 2)

        self.filtro_agend_status = QComboBox()
        self.filtro_agend_status.addItems(["Todos os Status", "Agendada", "Concluída", "Reposição", "Cancelada"])
        self.filtro_agend_status.currentIndexChanged.connect(self._aplicar_filtro_agendamentos)
        barra.addWidget(self.filtro_agend_status, 1)

        btn_concluir = QPushButton("✅ Concluir")
        btn_concluir.setObjectName("btnSucesso")
        btn_concluir.clicked.connect(lambda: self.alterar_status_agendamento("concluida"))
        barra.addWidget(btn_concluir)

        btn_agendar = QPushButton("⏳ Agendar")
        btn_agendar.setObjectName("btnSecundario")
        btn_agendar.clicked.connect(lambda: self.alterar_status_agendamento("agendada"))
        barra.addWidget(btn_agendar)

        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.setObjectName("btnPerigo")
        btn_cancelar.clicked.connect(lambda: self.alterar_status_agendamento("cancelada"))
        barra.addWidget(btn_cancelar)

        btn_csv = QPushButton("📥 Exportar CSV")
        btn_csv.setObjectName("btnSecundario")
        btn_csv.clicked.connect(lambda: self.exportar_tabela_csv(self.t_agend, "agendamentos_reclass.csv"))
        barra.addWidget(btn_csv)

        layout.addLayout(barra)

        # Filtro opcional de período, sem alterar a visualização padrão
        periodo = QHBoxLayout()
        periodo.setSpacing(8)
        self.filtro_agend_periodo = QCheckBox("Filtrar período")
        self.filtro_agend_periodo.setToolTip("Quando marcado, mostra apenas agendamentos entre as datas selecionadas.")
        self.filtro_agend_periodo.toggled.connect(self._aplicar_filtro_agendamentos)
        periodo.addWidget(self.filtro_agend_periodo)
        periodo.addWidget(QLabel("De"))
        self.filtro_agend_data_ini = QDateEdit()
        self.filtro_agend_data_ini.setCalendarPopup(True)
        self.filtro_agend_data_ini.setDisplayFormat("dd/MM/yyyy")
        self.filtro_agend_data_ini.setDate(QDate.currentDate().addDays(-30))
        self.filtro_agend_data_ini.dateChanged.connect(self._aplicar_filtro_agendamentos)
        periodo.addWidget(self.filtro_agend_data_ini)
        periodo.addWidget(QLabel("até"))
        self.filtro_agend_data_fim = QDateEdit()
        self.filtro_agend_data_fim.setCalendarPopup(True)
        self.filtro_agend_data_fim.setDisplayFormat("dd/MM/yyyy")
        self.filtro_agend_data_fim.setDate(QDate.currentDate().addDays(30))
        self.filtro_agend_data_fim.dateChanged.connect(self._aplicar_filtro_agendamentos)
        periodo.addWidget(self.filtro_agend_data_fim)
        periodo.addStretch()
        dica_periodo = QLabel("O filtro fica desativado até ser marcado.")
        dica_periodo.setStyleSheet(f"color: {TEXTO_MUTED}; font-size: 11px;")
        periodo.addWidget(dica_periodo)
        layout.addLayout(periodo)

        # Tabela
        colunas = ["ID", "Aluno", "Aula", "Data", "Horário", "Status"]
        self.t_agend = QTableWidget(0, len(colunas))
        self.t_agend.setHorizontalHeaderLabels(colunas)
        self.t_agend.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.t_agend.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.t_agend.setAlternatingRowColors(True)
        self.t_agend.verticalHeader().setVisible(False)
        self.t_agend.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.t_agend.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        # Menu de contexto com botão direito
        self.t_agend.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.t_agend.customContextMenuRequested.connect(self._menu_contexto_agendamentos)

        layout.addWidget(self.t_agend)
        self.abas.addTab(aba, "📝 Agendamentos")

    # ------------------------------------------------------
    # ABA 4: ALUNOS
    # ------------------------------------------------------
    def _criar_aba_alunos(self):
        aba = QWidget()
        layout = QVBoxLayout(aba)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(12)

        barra = QHBoxLayout()
        self.filtro_aluno_busca = QLineEdit()
        self.filtro_aluno_busca.setPlaceholderText("🔍 Filtrar por nome ou e-mail...")
        self.filtro_aluno_busca.textChanged.connect(self._aplicar_filtro_alunos)
        barra.addWidget(self.filtro_aluno_busca, 3)

        btn_csv = QPushButton("📥 Exportar CSV")
        btn_csv.setObjectName("btnSecundario")
        btn_csv.clicked.connect(lambda: self.exportar_tabela_csv(self.t_alunos, "alunos_reclass.csv"))
        barra.addWidget(btn_csv)
        layout.addLayout(barra)

        colunas = ["ID", "Nome do Aluno", "E-mail", "Cadastrado em", "Total de Agendamentos"]
        self.t_alunos = QTableWidget(0, len(colunas))
        self.t_alunos.setHorizontalHeaderLabels(colunas)
        self.t_alunos.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.t_alunos.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.t_alunos.setAlternatingRowColors(True)
        self.t_alunos.verticalHeader().setVisible(False)
        self.t_alunos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.t_alunos.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        self.t_alunos.doubleClicked.connect(self.abrir_detalhes_aluno)
        self.t_alunos.setToolTip("Dê dois cliques em um aluno para abrir seu perfil e histórico de aulas.")
        layout.addWidget(self.t_alunos)
        self.abas.addTab(aba, "👥 Alunos")

    # ------------------------------------------------------
    # CARREGAMENTO E SINCRONIZAÇÃO DE DADOS
    # ------------------------------------------------------
    def carregar_dados(self):
        try:
            # 1. Carregar Aulas e Ocupação
            aulas = consultar("""
                SELECT a.id, a.titulo, a.data, a.horario, a.unidade, a.vagas, a.observacoes,
                       (SELECT COUNT(*) FROM agendamentos g
                         WHERE g.aula = a.titulo
                           AND g.data = a.data
                           AND g.horario = a.horario
                           AND g.status <> 'cancelada') AS ocupadas
                FROM aulas a
                ORDER BY a.data DESC, a.horario DESC
            """)
            self.cache_aulas = aulas

            # 2. Carregar Agendamentos com Nome do Aluno
            agendamentos = consultar("""
                SELECT g.id, g.id_aluno, u.nome AS aluno_nome, g.aula, g.data, g.horario, g.status
                FROM agendamentos g
                LEFT JOIN usuarios u ON u.id = g.id_aluno
                ORDER BY g.id DESC
            """)
            self.cache_agendamentos = agendamentos

            # 3. Carregar Alunos
            alunos = consultar("""
                SELECT u.id, u.nome, u.email, u.data_cadastro,
                       (SELECT COUNT(*) FROM agendamentos g WHERE g.id_aluno = u.id) AS total_agend
                FROM usuarios u
                WHERE u.tipo_usuario = 'aluno'
                ORDER BY u.nome ASC
            """)
            self.cache_alunos = alunos

            # 4. Atualizar Cartões KPI
            total_vagas = sum((a["vagas"] or 0) for a in aulas)
            total_ocupadas = sum(a["ocupadas"] for a in aulas)
            taxa_ocup = round(total_ocupadas * 100 / total_vagas) if total_vagas else 0
            vazias = sum(1 for a in aulas if a["ocupadas"] == 0)

            self.kpi_aulas.definir(len(aulas), f"{sum(1 for a in aulas if a['ocupadas'] > 0)} com alunos")
            qtd_agendadas = sum(1 for g in agendamentos if (g.get("status") or "agendada") == "agendada")
            qtd_concluidas = sum(1 for g in agendamentos if (g.get("status") or "agendada") == "concluida")
            qtd_repor = sum(1 for g in agendamentos if (g.get("status") or "agendada") == "repor")
            self.kpi_agend.definir(len(agendamentos), f"{qtd_agendadas} agendados · {qtd_concluidas} concluídos · {qtd_repor} a repor")
            self.kpi_ocup.definir(f"{taxa_ocup}%", f"{total_ocupadas} de {total_vagas} vagas preenchidas")
            self.kpi_vagas.definir(total_vagas, f"{total_vagas - total_ocupadas} vagas livres")
            self.kpi_vazias.definir(vazias, "Aulas com 0 agendamentos")
            self.kpi_alunos.definir(len(alunos), "Estudantes ativos")

            # 5. Atualizar Gráficos
            # Gráfico de Status
            status_counts = {"Agendada": 0, "Concluída": 0, "Reposição": 0, "Cancelada": 0}
            for g in agendamentos:
                st = g["status"] or "agendada"
                if st == "concluida":
                    status_counts["Concluída"] += 1
                elif st == "repor":
                    status_counts["Reposição"] += 1
                elif st == "cancelada":
                    status_counts["Cancelada"] += 1
                else:
                    status_counts["Agendada"] += 1
            self.g_status.grafico.definir_dados(list(status_counts.items()))

            # Gráfico de Unidades
            unid_map = {}
            for a in aulas:
                u = (a["unidade"] or "Indefinida").replace("Unidade ", "")
                unid_map[u] = unid_map.get(u, 0) + a["ocupadas"]
            self.g_unidade.grafico.definir_dados(list(unid_map.items()))

            # Gráfico de Meses
            mes_map = {}
            for g in agendamentos:
                data_agendamento = converter_data(g.get("data"))
                if data_agendamento:
                    chave_mes = data_agendamento.strftime("%Y-%m")
                    mes_map[chave_mes] = mes_map.get(chave_mes, 0) + 1
            meses_recentes = sorted(mes_map.items())[-8:]
            dados_meses = [(datetime.strptime(chave, "%Y-%m").strftime("%m/%y"), total) for chave, total in meses_recentes]
            self.g_mes.grafico.definir_dados(dados_meses)

            # 6. Atualizar Unidades no Combo de Filtro de Aulas
            unidades_existentes = sorted(list(set(a["unidade"] for a in aulas if a.get("unidade"))))
            curr = self.filtro_aula_unidade.currentText()
            self.filtro_aula_unidade.blockSignals(True)
            self.filtro_aula_unidade.clear()
            self.filtro_aula_unidade.addItem("Todas as Unidades")
            for u in unidades_existentes:
                self.filtro_aula_unidade.addItem(u)
            if curr in unidades_existentes:
                self.filtro_aula_unidade.setCurrentText(curr)
            self.filtro_aula_unidade.blockSignals(False)

            # 7. Preencher Tabelas
            self._aplicar_filtro_aulas()
            self._aplicar_filtro_agendamentos()
            self._aplicar_filtro_alunos()
            self._atualizar_painel_agenda()

            hora_agora = datetime.now().strftime("%H:%M:%S")
            self.status_pill.setText("● Banco sincronizado")
            self.status_pill.setStyleSheet("")
            self.lbl_sub_dashboard.setText(f"Resumo de {date.today().strftime('%d/%m/%Y')} · última sincronização às {hora_agora}")
            self.barra_status.showMessage(f"Dados atualizados às {hora_agora} | {len(aulas)} aulas | {len(agendamentos)} agendamentos | Ctrl+R para atualizar.")

        except pymysql.MySQLError as erro:
            self.status_pill.setText("● Erro de conexão MySQL")
            self.status_pill.setStyleSheet("background: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA; border-radius: 12px; padding: 4px 10px; font-size: 11px; font-weight: 600;")
            self.barra_status.showMessage(f"Erro no banco MySQL: {erro}")

    def _atualizar_painel_agenda(self):
        """Atualiza próximos eventos e alertas sem fazer novas consultas SQL."""
        hoje = date.today()
        proximas = []
        for aula in self.cache_aulas:
            data_aula = converter_data(aula.get("data"))
            if data_aula is not None and data_aula >= hoje:
                proximas.append((data_aula, fmt_hora(aula.get("horario")), aula))
        proximas.sort(key=lambda item: (item[0], item[1]))
        proximas = proximas[:8]

        self.t_proximas.setRowCount(len(proximas))
        for row, (data_aula, hora, aula) in enumerate(proximas):
            ocupadas = int(aula.get("ocupadas") or 0)
            vagas = int(aula.get("vagas") or 0)
            livres = max(vagas - ocupadas, 0)
            valores = [data_aula.strftime("%d/%m"), hora, aula.get("titulo") or "-", f"{livres} livres"]
            for col, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if col == 0 and data_aula == hoje:
                    item.setForeground(QBrush(QColor(AZUL_PRIMARIO)))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                self.t_proximas.setItem(row, col, item)

        alertas = []
        futuras = [a for a in self.cache_aulas if (converter_data(a.get("data")) or date.min) >= hoje]
        sem_alunos = sum(1 for a in futuras if int(a.get("ocupadas") or 0) == 0)
        quase_cheias = sum(
            1 for a in futuras
            if int(a.get("vagas") or 0) > 0
            and int(a.get("ocupadas") or 0) / int(a.get("vagas") or 1) >= 0.9
        )
        atrasados = sum(
            1 for g in self.cache_agendamentos
            if (g.get("status") or "agendada") == "agendada"
            and converter_data(g.get("data")) is not None
            and converter_data(g.get("data")) < hoje
        )
        if sem_alunos:
            alertas.append(f"• {sem_alunos} aula(s) futura(s) ainda sem alunos.")
        if quase_cheias:
            alertas.append(f"• {quase_cheias} aula(s) com 90% ou mais das vagas ocupadas.")
        if atrasados:
            alertas.append(f"• {atrasados} agendamento(s) antigo(s) ainda marcado(s) como agendado(s).")
        if not alertas:
            alertas.append("✓ Nenhum alerta operacional no momento. Continue acompanhando os próximos agendamentos.")
        self.lbl_alertas.setText("\n\n".join(alertas))

    # ------------------------------------------------------
    # FILTROS E PREENCHIMENTO DE TABELAS
    # ------------------------------------------------------
    def _aplicar_filtro_aulas(self):
        termo = self.filtro_aula_busca.text().strip().lower()
        unidade_sel = self.filtro_aula_unidade.currentText()

        filtradas = []
        for a in self.cache_aulas:
            if termo and termo not in str(a.get("titulo", "")).lower():
                continue
            if unidade_sel != "Todas as Unidades" and a.get("unidade") != unidade_sel:
                continue
            filtradas.append(a)

        self.t_aulas.setRowCount(len(filtradas))
        for row, a in enumerate(filtradas):
            vagas = a.get("vagas") or 0
            ocup = a.get("ocupadas", 0)
            pct = round(ocup * 100 / vagas) if vagas else 0

            self.t_aulas.setItem(row, 0, self._celula(a["id"]))
            self.t_aulas.setItem(row, 1, self._celula(a["titulo"]))
            self.t_aulas.setItem(row, 2, self._celula(fmt_data(a["data"])))
            self.t_aulas.setItem(row, 3, self._celula(fmt_hora(a["horario"])))
            self.t_aulas.setItem(row, 4, self._celula(a["unidade"]))
            self.t_aulas.setItem(row, 5, self._celula(f"{ocup} / {vagas}"))

            barra = QProgressBar()
            barra.setRange(0, 100)
            barra.setValue(min(pct, 100))
            barra.setFormat(f"{pct}%")
            if pct >= 100:
                barra.setStyleSheet(f"QProgressBar::chunk {{ background-color: {VERMELHO_PERIGO}; border-radius: 6px; }}")
            elif pct >= 70:
                barra.setStyleSheet(f"QProgressBar::chunk {{ background-color: {AMARELO_ALERTA}; border-radius: 6px; }}")
            else:
                barra.setStyleSheet(f"QProgressBar::chunk {{ background-color: {VERDE_SUCESSO}; border-radius: 6px; }}")

            self.t_aulas.setCellWidget(row, 6, barra)

    def _aplicar_filtro_agendamentos(self):
        termo = self.filtro_agend_busca.text().strip().lower()
        status_sel = self.filtro_agend_status.currentText().lower()

        filtrados = []
        for g in self.cache_agendamentos:
            st = (g.get("status") or "agendada").lower()
            if status_sel != "todos os status":
                if status_sel == "agendada" and st != "agendada":
                    continue
                elif status_sel == "concluída" and st != "concluida":
                    continue
                elif status_sel == "reposição" and st != "repor":
                    continue
                elif status_sel == "cancelada" and st != "cancelada":
                    continue

            nome = str(g.get("aluno_nome") or "").lower()
            aula = str(g.get("aula") or "").lower()
            if termo and (termo not in nome and termo not in aula):
                continue

            if self.filtro_agend_periodo.isChecked():
                data_registro = converter_data(g.get("data"))
                data_ini = self.filtro_agend_data_ini.date().toPyDate()
                data_fim = self.filtro_agend_data_fim.date().toPyDate()
                if data_ini > data_fim:
                    continue
                if data_registro is None or not (data_ini <= data_registro <= data_fim):
                    continue

            filtrados.append(g)

        self.t_agend.setRowCount(len(filtrados))
        for row, g in enumerate(filtrados):
            st = g.get("status") or "agendada"

            badge = QLabel(st.capitalize())
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if st == "concluida":
                badge.setStyleSheet("background: #ECFDF5; color: #047857; font-weight: 700; border-radius: 6px; padding: 4px;")
            elif st == "cancelada":
                badge.setStyleSheet("background: #FEF2F2; color: #B91C1C; font-weight: 700; border-radius: 6px; padding: 4px;")
            else:
                badge.setStyleSheet("background: #FEF3C7; color: #B45309; font-weight: 700; border-radius: 6px; padding: 4px;")

            self.t_agend.setItem(row, 0, self._celula(g["id"]))
            self.t_agend.setItem(row, 1, self._celula(g.get("aluno_nome") or f"Aluno #{g.get('id_aluno')}"))
            self.t_agend.setItem(row, 2, self._celula(g.get("aula")))
            self.t_agend.setItem(row, 3, self._celula(fmt_data(g.get("data"))))
            self.t_agend.setItem(row, 4, self._celula(fmt_hora(g.get("horario"))))
            self.t_agend.setCellWidget(row, 5, badge)

    def _aplicar_filtro_alunos(self):
        termo = self.filtro_aluno_busca.text().strip().lower()

        filtrados = []
        for u in self.cache_alunos:
            nome = str(u.get("nome") or "").lower()
            email = str(u.get("email") or "").lower()
            if termo and (termo not in nome and termo not in email):
                continue
            filtrados.append(u)

        self.t_alunos.setRowCount(len(filtrados))
        for row, u in enumerate(filtrados):
            self.t_alunos.setItem(row, 0, self._celula(u["id"]))
            self.t_alunos.setItem(row, 1, self._celula(u["nome"]))
            self.t_alunos.setItem(row, 2, self._celula(u["email"]))
            self.t_alunos.setItem(row, 3, self._celula(fmt_data(u["data_cadastro"])))
            self.t_alunos.setItem(row, 4, self._celula(f"{u.get('total_agend', 0)} reposições"))

    def _celula(self, texto):
        item = QTableWidgetItem(str(texto if texto is not None else "-"))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item

    # ------------------------------------------------------
    # AÇÕES DO USUÁRIO (CRIAR, EXCLUIR, ATUALIZAR STATUS)
    # ------------------------------------------------------
    def abrir_detalhes_aluno(self):
        row = self.t_alunos.currentRow()
        if row < 0 or self.t_alunos.item(row, 0) is None:
            return
        try:
            aluno_id = int(self.t_alunos.item(row, 0).text())
        except (ValueError, AttributeError):
            return
        aluno = next((item for item in self.cache_alunos if int(item.get("id") or 0) == aluno_id), None)
        if aluno:
            DialogDetalheAluno(aluno, self).exec()

    def exportar_tabela_ativa(self):
        indice = self.abas.currentIndex()
        tabelas = {
            1: (getattr(self, "t_aulas", None), "aulas_reclass.csv"),
            2: (getattr(self, "t_agend", None), "agendamentos_reclass.csv"),
            3: (getattr(self, "t_alunos", None), "alunos_reclass.csv"),
        }
        tabela, nome = tabelas.get(indice, (None, None))
        if tabela is None:
            QMessageBox.information(self, "Exportar", "Abra a aba Aulas, Agendamentos ou Alunos para exportar os dados.")
            return
        self.exportar_tabela_csv(tabela, nome)

    def abrir_dialog_nova_aula(self):
        dialog = DialogNovaAula(self)
        if dialog.exec():
            self.carregar_dados()

    def abrir_inscritos_selecionado(self):
        row = self.t_aulas.currentRow()
        if row < 0:
            QMessageBox.information(self, "Aviso", "Selecione uma aula na tabela para ver os inscritos.")
            return

        aula_id = int(self.t_aulas.item(row, 0).text())
        aula = next((a for a in self.cache_aulas if a["id"] == aula_id), None)
        if aula:
            dialog = DialogInscritos(aula, self)
            dialog.exec()
            self.carregar_dados()

    def excluir_aula_selecionada(self):
        row = self.t_aulas.currentRow()
        if row < 0:
            QMessageBox.information(self, "Aviso", "Selecione uma aula na tabela para excluir.")
            return

        aula_id = self.t_aulas.item(row, 0).text()
        titulo = self.t_aulas.item(row, 1).text()

        resp = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Tem certeza que deseja excluir a aula '{titulo}' (ID {aula_id})?\n"
            "Essa ação não poderá ser desfeita.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if resp == QMessageBox.StandardButton.Yes:
            try:
                executar("DELETE FROM aulas WHERE id = %s", (aula_id,))
                self.carregar_dados()
                self.barra_status.showMessage(f"Aula '{titulo}' excluída com sucesso.")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível excluir a aula: {e}")

    def alterar_status_agendamento(self, novo_status):
        row = self.t_agend.currentRow()
        if row < 0:
            QMessageBox.information(self, "Aviso", "Selecione um agendamento na tabela.")
            return

        agend_id = self.t_agend.item(row, 0).text()
        try:
            executar("UPDATE agendamentos SET status = %s WHERE id = %s", (novo_status, agend_id))
            self.carregar_dados()
            self.barra_status.showMessage(f"Status do agendamento #{agend_id} alterado para '{novo_status}'.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível atualizar o status: {e}")

    def _menu_contexto_agendamentos(self, ponto):
        menu = QMenu(self)
        acao_concluir = QAction("✅ Marcar como Concluída", self)
        acao_concluir.triggered.connect(lambda: self.alterar_status_agendamento("concluida"))

        acao_agendada = QAction("⏳ Marcar como Agendada", self)
        acao_agendada.triggered.connect(lambda: self.alterar_status_agendamento("agendada"))

        acao_cancelar = QAction("❌ Cancelar Agendamento", self)
        acao_cancelar.triggered.connect(lambda: self.alterar_status_agendamento("cancelada"))

        menu.addAction(acao_concluir)
        menu.addAction(acao_agendada)
        menu.addAction(acao_cancelar)
        menu.exec(self.t_agend.mapToGlobal(ponto))

    # ------------------------------------------------------
    # EXPORTAÇÃO PARA CSV
    # ------------------------------------------------------
    def exportar_tabela_csv(self, tabela, nome_sugerido):
        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório CSV", nome_sugerido, "Arquivos CSV (*.csv)")
        if not caminho:
            return

        try:
            with open(caminho, mode="w", newline="", encoding="utf-8-sig") as arq:
                escritor = csv.writer(arq, delimiter=";")
                # Cabeçalhos
                headers = [tabela.horizontalHeaderItem(c).text() for c in range(tabela.columnCount())]
                escritor.writerow(headers)

                # Linhas
                for r in range(tabela.rowCount()):
                    linha = []
                    for c in range(tabela.columnCount()):
                        item = tabela.item(r, c)
                        if item:
                            linha.append(item.text())
                        else:
                            widget = tabela.cellWidget(r, c)
                            if isinstance(widget, QLabel):
                                linha.append(widget.text())
                            elif isinstance(widget, QProgressBar):
                                linha.append(f"{widget.value()}%")
                            else:
                                linha.append("")
                    escritor.writerow(linha)

            QMessageBox.information(self, "Sucesso", f"Dados exportados com sucesso para:\n{caminho}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao exportar CSV: {e}")


# ----------------------------------------------------------
# CONTROLE DE INSTÂNCIA ÚNICA (SOCKET LOCAL)
# ----------------------------------------------------------
NOME_SOCKET = "reclass_desktop_single_instance_socket"


class ServidorInstanciaUnica(QLocalServer):
    def __init__(self, janela, parent=None):
        super().__init__(parent)
        self.janela = janela
        self.newConnection.connect(self._tratar_conexao)

    def _tratar_conexao(self):
        socket = self.nextPendingConnection()
        if socket:
            socket.readyRead.connect(lambda: self._ler_mensagem(socket))

    def _ler_mensagem(self, socket):
        socket.readAll()
        socket.disconnectFromServer()
        # Traz a janela para frente e atualiza os dados
        self.janela.showNormal()
        self.janela.raise_()
        self.janela.activateWindow()
        self.janela.carregar_dados()


# ----------------------------------------------------------
# PONTO DE ENTRADA PRINCIPAL
# ----------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    # Tenta conectar à instância já em execução
    socket = QLocalSocket()
    socket.connectToServer(NOME_SOCKET)
    if socket.waitForConnected(500):
        # Envia sinal para trazer para frente e encerra esta chamada
        socket.write(b"FOCUS")
        socket.waitForBytesWritten(500)
        socket.disconnectFromServer()
        sys.exit(0)

    # Inicia como instância primária
    QLocalServer.removeServer(NOME_SOCKET)
    janela = JanelaPrincipal()

    servidor = ServidorInstanciaUnica(janela, app)
    servidor.listen(NOME_SOCKET)

    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
