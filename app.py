import streamlit as st
import pandas as pd
import os
from fpdf import FPDF  # Librería para generar PDF

# Función para inicializar archivos CSV si no existen
def initialize_csv(file_name, headers):
    if not os.path.exists(file_name):
        df = pd.DataFrame(columns=headers)
        df.to_csv(file_name, index=False)

# Inicialización de archivos CSV
initialize_csv("stock.csv", ["id_stock", "id_producto", "cantidad", "descripcion", "precio"])
initialize_csv("productos.csv", ["id_producto", "descripcion", "precio", "id_proveedor"])
initialize_csv("proveedores.csv", ["id_proveedor", "nombre", "direccion", "telefono", "email"])
initialize_csv("compras.csv", ["id_compra", "id_proveedor", "productos", "fecha", "total"])
initialize_csv("ventas.csv", ["id_venta", "fecha", "productos", "total", "metodo_pago", "factura"])

# Función para cargar datos desde un archivo CSV
def load_csv(file_name):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        st.error(f"El archivo {file_name} no existe.")
        return pd.DataFrame()

# Función para guardar datos en un archivo CSV
def save_csv(df, file_name):
    df.to_csv(file_name, index=False)

# Función para generar factura como PDF
def generate_invoice_pdf(venta_id, productos, cantidades, total, stock_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Factura ID: {venta_id}", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Productos vendidos:", ln=True)
    
    for producto_id, cantidad in cantidades.items():
        producto_info = stock_df[stock_df["id_producto"] == producto_id]
        descripcion = producto_info["descripcion"].values[0]
        precio = producto_info["precio"].values[0]
        subtotal = cantidad * precio
        pdf.cell(200, 10, txt=f"- {descripcion} (Cantidad: {cantidad}) - Subtotal: ${subtotal:.2f}", ln=True)
    
    iva = total * 0.27
    total_con_iva = total + iva
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Subtotal: ${total:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"IVA (27%): ${iva:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total con IVA: ${total_con_iva:.2f}", ln=True)
    
    factura_dir = "facturas"
    os.makedirs(factura_dir, exist_ok=True)
    pdf_path = os.path.join(factura_dir, f"factura_{venta_id}.pdf")
    pdf.output(pdf_path)
    
    return pdf_path

# Interfaz principal
def main():
    st.title("Sistema de Ventas de Repuestos Sanitarios")

    menu = ["Gestión de Stock", "Gestión de Proveedores", "Compras a Proveedores", "Nueva Venta", "Ventas"]
    choice = st.sidebar.selectbox("Navegación", menu)

    if choice == "Gestión de Stock":
        st.header("Gestión de Stock")
        stock_df = load_csv("stock.csv")
        if stock_df.empty:
            st.info("No hay productos en el stock.")
        else:
            st.dataframe(stock_df)

        with st.form("Agregar Producto"):
            st.subheader("Agregar Producto")
            id_producto = st.text_input("ID Producto")
            descripcion = st.text_input("Descripción")
            precio = st.number_input("Precio", min_value=0.0)
            cantidad = st.number_input("Cantidad", min_value=0, step=1)
            submit = st.form_submit_button("Agregar")
            if submit:
                new_row = {"id_stock": len(stock_df) + 1, "id_producto": id_producto, "cantidad": cantidad, "descripcion": descripcion, "precio": precio}
                stock_df = pd.concat([stock_df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(stock_df, "stock.csv")
                st.success("Producto agregado exitosamente.")

    elif choice == "Gestión de Proveedores":
        st.header("Gestión de Proveedores")
        proveedores_df = load_csv("proveedores.csv")
        if proveedores_df.empty:
            st.info("No hay proveedores registrados.")
        else:
            st.dataframe(proveedores_df)

        with st.form("Agregar Proveedor"):
            st.subheader("Agregar Proveedor")
            id_proveedor = st.text_input("ID Proveedor")
            nombre = st.text_input("Nombre")
            direccion = st.text_input("Dirección")
            telefono = st.text_input("Teléfono")
            email = st.text_input("Email")
            submit = st.form_submit_button("Agregar")
            if submit:
                new_row = {"id_proveedor": id_proveedor, "nombre": nombre, "direccion": direccion, "telefono": telefono, "email": email}
                proveedores_df = pd.concat([proveedores_df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(proveedores_df, "proveedores.csv")
                st.success("Proveedor agregado exitosamente.")

    elif choice == "Compras a Proveedores":
        st.header("Compras a Proveedores")
        compras_df = load_csv("compras.csv")
        proveedores_df = load_csv("proveedores.csv")
        stock_df = load_csv("stock.csv")

        if proveedores_df.empty:
            st.warning("No hay proveedores registrados. Registra uno primero.")
            return

        with st.form("Registrar Compra"):
            st.subheader("Registrar Compra")
            id_proveedor = st.selectbox("Seleccionar Proveedor", proveedores_df["id_proveedor"])
            productos_comprados = st.multiselect("Seleccionar Productos", stock_df["id_producto"].tolist())
            cantidades = {
                prod: st.number_input(f"Cantidad para {prod}", min_value=0, step=1)
                for prod in productos_comprados
            }
            submit = st.form_submit_button("Registrar Compra")
            if submit:
                total = sum(
                    cantidades[prod] * stock_df[stock_df["id_producto"] == prod]["precio"].values[0]
                    for prod in productos_comprados
                )
                new_row = {
                    "id_compra": len(compras_df) + 1,
                    "id_proveedor": id_proveedor,
                    "productos": str(productos_comprados),
                    "fecha": pd.Timestamp.now().strftime("%Y-%m-%d"),
                    "total": total,
                }
                compras_df = pd.concat([compras_df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(compras_df, "compras.csv")
                st.success("Compra registrada exitosamente.")

        if not compras_df.empty:
            st.dataframe(compras_df)

    elif choice == "Nueva Venta":
        st.header("Nueva Venta")
        stock_df = load_csv("stock.csv")
        ventas_df = load_csv("ventas.csv")

        if stock_df.empty:
            st.warning("El stock está vacío. Agrega productos primero.")
            return

        productos_seleccionados = st.multiselect(
            "Seleccionar Productos",
            stock_df["id_producto"].tolist(),
            format_func=lambda x: f"{x} - {stock_df[stock_df['id_producto'] == x]['descripcion'].values[0]}"
        )

        cantidades = {
            prod: st.number_input(f"Cantidad para {prod} ({stock_df[stock_df['id_producto'] == prod]['descripcion'].values[0]})", min_value=0, step=1)
            for prod in productos_seleccionados
        }

        if st.button("Registrar Venta"):
            total = sum(
                cantidades[prod] * stock_df[stock_df["id_producto"] == prod]["precio"].values[0]
                for prod in productos_seleccionados
            )
            new_id_venta = int(ventas_df["id_venta"].max() + 1 if not ventas_df.empty else 1)
            pdf_path = generate_invoice_pdf(new_id_venta, productos_seleccionados, cantidades, total, stock_df)

            nueva_venta = {
                "id_venta": new_id_venta,
                "fecha": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "productos": str(productos_seleccionados),
                "total": total,
                "metodo_pago": "Efectivo",
                "factura": pdf_path,
            }
            ventas_df = pd.concat([ventas_df, pd.DataFrame([nueva_venta])], ignore_index=True)
            save_csv(ventas_df, "ventas.csv")
            st.success(f"Venta registrada exitosamente. Total: ${total:.2f}")
            st.info(f"Factura generada: {pdf_path}")

    elif choice == "Ventas":
        st.header("Ventas")
        ventas_df = load_csv("ventas.csv")

        if ventas_df.empty:
            st.warning("No hay ventas registradas.")
        else:
            for _, row in ventas_df.iterrows():
                st.write(f"ID Venta: {row['id_venta']}, Fecha: {row['fecha']}, Total: ${row['total']:.2f}")
                st.write(f"Productos: {row['productos']}")

                # Verificar si el archivo de la factura existe antes de intentar descargarlo
                if os.path.exists(row['factura']):
                    with open(row['factura'], "rb") as file:
                        st.download_button(
                            label="Descargar Factura",
                            data=file,
                            file_name=os.path.basename(row['factura'])
                        )
                else:
                    st.warning(f"El archivo de factura {row['factura']} no existe. Verifica su generación.")

if __name__ == "__main__":
    main()
