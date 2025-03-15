__authors__ = ['1668213','1665951','1668826']
__group__ = 'noneyet'

from utils_data import read_dataset, read_extended_dataset, crop_images, visualize_retrieval
from Kmeans import KMeans, get_colors
import numpy as np
from KNN import KNN


def retrieval_by_color(imatges, etiquetes, pregunta):
    
    imatges_resultants = []
    index = -1
    indices = []

    for imgAux, etqAux in zip(imatges, etiquetes):
        index += 1
        for e in etqAux:
            if e in pregunta:
                imatges_resultants.append(imgAux)
                indices.append(index)
                break;
    
    return np.array(imatges_resultants), indices

def retrieval_by_shape(imatges, etiquetes, pregunta):
    
    imatges_resultants = []
    index = -1
    indices = []
    
    for imgAux, etqAux in zip(imatges, etiquetes):
        index += 1
        if etqAux in pregunta:
            imatges_resultants.append(imgAux)
            indices.append(index)

    
    return np.array(imatges_resultants), indices

def retrieval_combined(imatges, etiquetes_color, etiquetes_shape, pregunta):
    
    imatges_resultants = []
    index = -1
    indices = []
    
    for imgAux, etq_colorAux, etq_shapeAux in zip(imatges, etiquetes_color, etiquetes_shape):
        index += 1
        for eColor in etq_colorAux:
            if eColor in pregunta:
                if etq_shapeAux in pregunta:
                    imatges_resultants.append(imgAux)
                    indices.append(index)
                    break;
    
    return np.array(imatges_resultants), indices


def get_shape_accuracy(etiquetes, ground_truth):
    valor = np.sum(etiquetes == ground_truth)
    total = etiquetes.shape[0]
    res = valor / total * 100
    percentatge = round(res, 2)
    return percentatge

def get_color_accuracy(etiquetes, ground_truth):
    valor = 0
    for colores, result in zip(etiquetes, ground_truth):
        iguales = all(item in colores for item in result)
        if iguales == True:
            valor += 1

    total = len(etiquetes)
    res = valor / total * 100
    percentatge = round(res, 2)
    return percentatge


if __name__ == '__main__':

    # Load all the images and GT
    train_imgs, train_class_labels, train_color_labels, test_imgs, test_class_labels, \
        test_color_labels = read_dataset(root_folder='./images/', gt_json='./images/gt.json')

    # List with all the existent classes
    classes = list(set(list(train_class_labels) + list(test_class_labels)))

    # Load extended ground truth
    imgs, class_labels, color_labels, upper, lower, background = read_extended_dataset()
    cropped_images = crop_images(imgs, upper, lower)

    # You can start coding your functions here


    print("Ejecutando test Kmeans")
    
    colores_correctos = []
    correccion_color = []
    resultados_color = []
    
    color = ["Green"]
    

    for imatge in test_imgs:
        kmean = KMeans(imatge, K=10)
        kmean.fit()
        colors = get_colors(kmean.centroids)
        resultados_color.append(colors)
           
        
        retrieval, indices = retrieval_by_color(test_imgs, resultados_color, color)
        
    for i in indices:
        colores_correctos.append(test_color_labels[i])
        correccion_color.append(True if color[0] in test_color_labels[i] else False)
    
    visualize_retrieval(retrieval, 15, title = color, info=colores_correctos, ok=correccion_color)


    print("Ejecutando test Kmeans - Cropped Images")
    
    colores_correctos = []
    correccion_color = []
    resultados_color = []
    color = ["Black"]
    

    for imatge in cropped_images:
        kmean = KMeans(imatge, K=4)
        kmean.fit()
        colors = get_colors(kmean.centroids)
        resultados_color.append(colors)
        
        
        retrieval, indices = retrieval_by_color(imgs, resultados_color, color)
        
    for i in indices:
        colores_correctos.append(color_labels[i])
        correccion_color.append(True if color[0] in color_labels[i] else False)
    
    
    visualize_retrieval(retrieval, 15, title = color, info=colores_correctos, ok=correccion_color)


    print("Ejecutando test KNN")
    
    formas_correctas = []
    correccion_forma = []
    
    forma = ["Shorts"]
    
    knn_results = KNN(train_imgs, train_class_labels)
    resultados_forma = knn_results.predict(test_imgs, 4)
    
    retrieval_forma, indices_forma = retrieval_by_shape(test_imgs, resultados_forma, forma)
    
    for i in indices_forma:
        formas_correctas.append(test_class_labels[i])
        correccion_forma.append(True if forma[0] in test_class_labels[i] else False)
        
    visualize_retrieval(retrieval_forma, 15, title = forma, info=formas_correctas, ok=correccion_forma)     


    print("Ejecutando test Combined")
    
    pregunta_combinada = [color[0], forma[0]]
    
    retrieval_combinado, indices_combinado = retrieval_combined(test_imgs, resultados_color, resultados_forma, pregunta_combinada)
    
    combinado_correcto = []
    
    for i in indices_combinado:
        test_color_labels[i].append(test_class_labels[i])
        combinado_correcto.append(test_color_labels[i])
    visualize_retrieval(retrieval_combinado, 15, title = pregunta_combinada, info = combinado_correcto)
    
    
    print("Shape accuracy:", get_shape_accuracy(resultados_forma, test_class_labels))
    print("Color accuracy:", get_color_accuracy(resultados_color, test_color_labels))
    
    
    
    
    
    

    
    

    