import gradio as gr

def calculate(n1, n2):
    try:
        n1 = float(n1)
        n2 = float(n2)

        total_sum = n1 + n2
        difference = n1 - n2
        product = n1 * n2
        division = n1 / n2 if n2 != 0 else "Infinity"

        return (
            f"Sum: {total_sum}\n"
            f"Difference: {difference}\n"
            f"Product: {product}\n"
            f"Division: {division}"
        )

    except:
        return "Invalid input! Please enter numbers."

# GUI Interface

app = gr.Interface(
    fn=calculate,
    inputs=[gr.Number(label="Enter first number"), gr.Number(label="Enter second number")],
    outputs="text",
    title="Simple Calculator (Gradio)",
)

app.launch()