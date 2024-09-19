import os
import ast
import graphviz


def extract_classes(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = []
            for n in node.body:
                if isinstance(n, ast.FunctionDef):
                    # Determine if the method is private or public
                    if n.name.startswith("__") and not n.name.endswith("__"):
                        visibility = "-"
                    else:
                        visibility = "+"

                    # Extracting function name and arguments with their types
                    method_name = n.name
                    args = []
                    for arg in n.args.args:
                        if isinstance(arg.annotation, ast.Name):
                            args.append(f"{arg.arg}: {arg.annotation.id}")
                        elif isinstance(arg.annotation, ast.Subscript):
                            if isinstance(arg.annotation.value, ast.Name):
                                args.append(
                                    f"{arg.arg}: {arg.annotation.value.id}[{arg.annotation.slice.value.id}]"
                                )
                        else:
                            args.append(arg.arg)
                    method_signature = f"{visibility} {method_name}({', '.join(args)})"
                    methods.append(method_signature)
            if methods:  # Only add classes with methods
                classes.append((node.name, methods))

    return classes


def create_class_diagram(classes_with_paths, output_file):
    dot = graphviz.Digraph(comment="Class Diagram", format="png")

    # Group classes by file
    classes_by_file = {}
    for file_path, class_name, methods in classes_with_paths:
        if file_path not in classes_by_file:
            classes_by_file[file_path] = []
        classes_by_file[file_path].append((class_name, methods))

    # Create subgraphs for each file
    for file_path, classes in classes_by_file.items():
        with dot.subgraph(name=f"cluster_{file_path}") as sub:
            sub.attr(label=file_path, style="filled", color="lightgrey")
            for class_name, methods in classes:
                # Create a label with methods listed vertically and prefixed with + or -
                label = f"{{ {class_name} | "
                label += "\\l".join(methods) + "\\l"  # Each method on a new line
                label += " }"
                sub.node(class_name, label, shape="record")

    dot.render(output_file)
    print(f"Class diagram saved to {output_file}.png")


def main():
    folder_path = "."
    output_file = "class_diagram"
    all_classes_with_paths = []

    # Read all Python files in the folder and subfolders
    for dirpath, dirnames, filenames in os.walk(folder_path):
        # Skip directories that start with "test"
        dirnames[:] = [d for d in dirnames if not d.startswith("test")]

        for filename in filenames:
            if filename.endswith(".py") and not filename.startswith("test"):
                file_path = os.path.join(dirpath, filename)
                print(f"Processing file: {file_path}")
                classes = extract_classes(file_path)
                for class_name, methods in classes:
                    all_classes_with_paths.append((file_path, class_name, methods))

    # Create the class diagram
    create_class_diagram(all_classes_with_paths, output_file)


if __name__ == "__main__":
    main()
