print("APP STARTING...")
import gradio as gr
import matplotlib.pyplot as plt

def bubble_sort_trace(arr):
    steps = []
    explanations = []
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            left, right = a[j], a[j+1]
            msg = f"Comparing {left} and {right}"
            if left > right:
                a[j], a[j+1] = a[j+1], a[j]
                msg += " → swapped"
            else:
                msg += " → no swap"
            steps.append(a.copy())
            explanations.append(msg)
    return steps, explanations

def make_figure(arr, title=""):
    fig, ax = plt.subplots(figsize=(7, 4))  
    ax.bar(range(len(arr)), arr)
    ax.set_xticks(range(len(arr)))
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_title(title)
    plt.tight_layout()
    return fig

def visualize_step(step_index, steps, explanations):
    if not steps:
        return None, "No steps available."

    step_index = max(0, min(step_index, len(steps)-1))
    arr = steps[step_index]
    fig = make_figure(arr, title=f"Step {step_index+1}")
    explanation = explanations[step_index]
    return fig, explanation

def run_sort_and_show_first(input_text):
    try:
        nums = [int(x.strip()) for x in input_text.split(",") if x.strip() != ""]
    except:
        return ("❌ Invalid input. Enter numbers like: 5, 3, 8, 1",
                gr.update(maximum=1, value=0),
                None,
                [],
                [])

    if len(nums) == 0:
        return ("Please enter at least one number.",
                gr.update(maximum=1, value=0),
                None,
                [],
                [])

    steps, explanations = bubble_sort_trace(nums)
    fig = None
    if steps:
        fig, _ = visualize_step(0, steps, explanations)

    summary = f"✅ Bubble Sort complete — total steps: {len(steps)}"
    slider_update = gr.update(maximum=len(steps)-1 if steps else 1, value=0)

    return summary, slider_update, fig, steps, explanations

def update_plot_from_slider(step_index, steps, explanations):
    fig, explanation = visualize_step(step_index, steps, explanations)
    return fig, explanation

def main():
    with gr.Blocks(css="""
        /* Title */
        #title { text-align: center; font-size: 2.2rem; color: white; }

        body { background: #1a1a1a !important; }

        /* Textboxes black + white text */
        .gr-textbox textarea {
            background-color: black !important;
            color: white !important;
            border: 1px solid #444 !important;
        }

        /* Markdown boxes (summary + explanation) */
        .gr-markdown {
            background-color: black !important;
            color: white !important;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #444;
        }

        /* Slider label */
        label {
            color: white !important;
        }

        /* Section boxes */
        .section-box {
            border: 1px solid #444 !important;
            padding: 12px;
            border-radius: 8px;
            background: #111 !important;
            color: white !important;
        }

        /* Center button */
        .center-btn { display: flex; justify-content: center; margin-top: 10px; }
    """) as demo:

        gr.Markdown("<h1 id='title'>🫧 Bubble Sort Visualizer</h1>")
        gr.Markdown("<p style='text-align:center; color:white;'>Created by Abdullah Hammad</p>")

        # Input row
        with gr.Row():
            input_box = gr.Textbox(label="Enter Numbers", placeholder="e.g. 4, 2, 7, 1")

        # Run button
        with gr.Row(elem_classes="center-btn"):
            run_btn = gr.Button("▶ Run Bubble Sort", size="lg")

        summary_out = gr.Markdown("")

        # Step slider
        step_slider = gr.Slider(0, 1, value=0, step=1, label="Step Number")

        explanation_out = gr.Markdown("Step explanation will appear here.", elem_classes="section-box")

        # Visualization full-width
        plot_out = gr.Plot(label="Visualization", elem_classes="section-box")

        steps_state = gr.State([])
        explanations_state = gr.State([])

        run_btn.click(
            run_sort_and_show_first,
            inputs=[input_box],
            outputs=[summary_out, step_slider, plot_out, steps_state, explanations_state]
        )

        step_slider.change(
            update_plot_from_slider,
            inputs=[step_slider, steps_state, explanations_state],
            outputs=[plot_out, explanation_out]
        )

    print("ABOUT TO LAUNCH")
    return demo

if __name__ == "__main__":
    print("APP STARTING…")
    demo = main()
    demo.launch(server_name="0.0.0.0", server_port=7860)
