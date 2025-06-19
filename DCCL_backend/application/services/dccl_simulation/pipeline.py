class SimulationPipeline:
    def __init__(self, input_data,user_id):
        self.input_data = input_data
        self.user_id = user_id

    def run(self):
        elements = self.input_data.elements
        resonator_param = self.input_data.resonatorParam
        fft_param = self.input_data.fastFourierTransformParam
        distance = self.input_data.distance
        angle = self.input_data.angle

        effective_area = calculate_effective_area(elements, resonator_param)
        transfer_matrix = calculate_transfer_matrix(elements, distance, angle, effective_area)
        gain_result = calculate_gain(resonator_param, transfer_matrix)
        fox_li_result = fox_li_iteration(elements, gain_result, fft_param)

        return {
            "effective_area": effective_area,
            "transfer_matrix": transfer_matrix.tolist(),  # 如果是 numpy，要转 list
            "gain_result": gain_result,
            "fox_li_result": fox_li_result
        }