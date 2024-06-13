"""
    HOW TO USE
    First initialize the temperature sensors
    Then you can pass the sensors to the read_temp function
"""

from machine import Pin
from machine import ADC
from machine import DAC
from math import log

import machine
import utime

class TemperatureSensor:

    adc_V_lookup = [0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 1.000588, 0.9511765, 0.9388236, 0.8276471, 0.8029412, 0.735, 0.8585295, 0.6361765, 0.7782353, 0.4817647, 0.432353, 0.3705883, 0.6855883, 0.2717647, 0.2347059, 0.6176471, 0.09882354, 0.02470588, 0.5497059, 1.099412, 1.1025, 1.105588, 1.108677, 1.111765, 1.114853, 1.117941, 1.121029, 1.124118, 1.128235, 1.132353, 1.136471, 1.140588, 1.144706, 1.148824, 1.151294, 1.153765, 1.156235, 1.158706, 1.161177, 1.165294, 1.169412, 1.17353, 1.176618, 1.179706, 1.182794, 1.185882, 1.188353, 1.190824, 1.193294, 1.195765, 1.198235, 1.202353, 1.206471, 1.210588, 1.214706, 1.218824, 1.222941, 1.226029, 1.229118, 1.232206, 1.235294, 1.238382, 1.241471, 1.244559, 1.247647, 1.250735, 1.253824, 1.256912, 1.26, 1.263088, 1.266176, 1.269265, 1.272353, 1.278529, 1.284706, 1.287794, 1.290882, 1.293971, 1.297059, 1.300147, 1.303235, 1.306324, 1.309412, 1.3125, 1.315588, 1.318676, 1.321765, 1.327941, 1.334118, 1.337206, 1.340294, 1.343382, 1.346471, 1.348529, 1.350588, 1.352647, 1.354706, 1.356765, 1.358824, 1.362941, 1.367059, 1.371176, 1.375294, 1.379412, 1.383529, 1.387647, 1.391765, 1.395882, 1.398971, 1.402059, 1.405147, 1.408235, 1.412353, 1.416471, 1.420588, 1.423059, 1.425529, 1.428, 1.430471, 1.432941, 1.437059, 1.441177, 1.445294, 1.449412, 1.453529, 1.457647, 1.461765, 1.465882, 1.47, 1.472471, 1.474941, 1.477412, 1.479882, 1.482353, 1.486471, 1.490588, 1.494706, 1.498824, 1.502941, 1.507059, 1.509529, 1.512, 1.514471, 1.516941, 1.519412, 1.52353, 1.527647, 1.531765, 1.534853, 1.537941, 1.541029, 1.544118, 1.546588, 1.549059, 1.551529, 1.554, 1.556471, 1.560588, 1.564706, 1.575, 1.572353, 1.575882, 1.579412, 1.582941, 1.586471, 1.59, 1.593529, 1.599706, 1.605882, 1.61, 1.614118, 1.618235, 1.620706, 1.623176, 1.625647, 1.628118, 1.630588, 1.634706, 1.638824, 1.642941, 1.647059, 1.651177, 1.655294, 1.657765, 1.660235, 1.662706, 1.665176, 1.667647, 1.673824, 1.68, 1.686177, 1.692353, 1.694824, 1.697294, 1.699765, 1.702235, 1.704706, 1.708824, 1.712941, 1.717059, 1.719118, 1.721177, 1.723235, 1.725294, 1.727353, 1.729412, 1.735588, 1.741765, 1.744853, 1.747941, 1.751029, 1.754118, 1.757206, 1.760294, 1.763382, 1.766471, 1.772647, 1.778824, 1.781912, 1.785, 1.788088, 1.791177, 1.794265, 1.797353, 1.800441, 1.80353, 1.806, 1.808471, 1.810941, 1.813412, 1.815882, 1.822059, 1.828235, 1.831324, 1.834412, 1.8375, 1.840588, 1.842647, 1.844706, 1.846765, 1.848824, 1.850882, 1.859118, 1.857882, 1.862824, 1.867765, 1.872706, 1.877647, 1.881765, 1.885882, 1.89, 1.894118, 1.898235, 1.902353, 1.904412, 1.90647, 1.908529, 1.910588, 1.912647, 1.914706, 1.920882, 1.927059, 1.931176, 1.935294, 1.939412, 1.9425, 1.945588, 1.948677, 1.951765, 1.954853, 1.957941, 1.96103, 1.964118, 1.966177, 1.968235, 1.970294, 1.972353, 1.974412, 1.976471, 1.982647, 1.988824, 1.991294, 1.993765, 1.996235, 1.998706, 2.001177, 2.005294, 2.009412, 2.01353, 2.016, 2.018471, 2.020941, 2.023412, 2.025882, 2.03, 2.034118, 2.038235, 2.050588, 2.052647, 2.054706, 2.056765, 2.058824, 2.060882, 2.062941, 2.06603, 2.069118, 2.072206, 2.075294, 2.087647, 2.090735, 2.093824, 2.096912, 2.1, 2.103088, 2.106177, 2.109265, 2.112353, 2.116471, 2.120588, 2.124706, 2.127177, 2.129647, 2.132118, 2.134588, 2.137059, 2.141176, 2.145294, 2.149412, 2.151882, 2.154353, 2.156824, 2.159294, 2.161765, 2.165882, 2.17, 2.174118, 2.180294, 2.186471, 2.188941, 2.191412, 2.193882, 2.196353, 2.198824, 2.205, 2.211177, 2.22353, 2.226, 2.228471, 2.230941, 2.233412, 2.235883, 2.237647, 2.239412, 2.241177, 2.242941, 2.244706, 2.246471, 2.248235, 2.251324, 2.254412, 2.2575, 2.260588, 2.263677, 2.266765, 2.269853, 2.272941, 2.279118, 2.285294, 2.288383, 2.291471, 2.294559, 2.297647, 2.300118, 2.302588, 2.305059, 2.307529, 2.31, 2.314118, 2.318235, 2.322353, 2.326471, 2.330588, 2.334706, 2.337794, 2.340883, 2.343971, 2.347059, 2.34953, 2.352, 2.354471, 2.356941, 2.359412, 2.361882, 2.364353, 2.366824, 2.369294, 2.371765, 2.375882, 2.38, 2.384118, 2.387206, 2.390294, 2.393382, 2.396471, 2.399559, 2.402647, 2.405735, 2.408823, 2.411912, 2.415, 2.418088, 2.421176, 2.424265, 2.427353, 2.430441, 2.433529, 2.437647, 2.441765, 2.445882, 2.448353, 2.450824, 2.453294, 2.455765, 2.458235, 2.461323, 2.464412, 2.4675, 2.470588, 2.474706, 2.478824, 2.482941, 2.487059, 2.491177, 2.495294, 2.497765, 2.500235, 2.502706, 2.505177, 2.507647, 2.510735, 2.513824, 2.516912, 2.52, 2.522471, 2.524941, 2.527412, 2.529882, 2.532353, 2.536471, 2.540588, 2.544706, 2.547177, 2.549647, 2.552118, 2.554588, 2.557059, 2.563235, 2.569412, 2.571177, 2.572941, 2.574706, 2.576471, 2.578235, 2.58, 2.581765, 2.587941, 2.594118, 2.597206, 2.600294, 2.603382, 2.606471, 2.60853, 2.610588, 2.612647, 2.614706, 2.616765, 2.618824, 2.622941, 2.627059, 2.631176, 2.633235, 2.635294, 2.637353, 2.639412, 2.641471, 2.643529, 2.646618, 2.649706, 2.652794, 2.655882, 2.658971, 2.662059, 2.665147, 2.668235, 2.67, 2.671765, 2.67353, 2.675294, 2.677059, 2.678824, 2.680588, 2.683676, 2.686765, 2.689853, 2.692941, 2.696029, 2.699118, 2.702206, 2.705294, 2.708382, 2.711471, 2.714559, 2.717647, 2.719412, 2.721177, 2.722941, 2.724706, 2.726471, 2.728235, 2.73, 2.736176, 2.742353, 2.744118, 2.745883, 2.747647, 2.749412, 2.751176, 2.752941, 2.754706, 2.756765, 2.758824, 2.760882, 2.762941, 2.765, 2.767059, 2.769529, 2.772, 2.774471, 2.776941, 2.779412, 2.781882, 2.784353, 2.786824, 2.789294, 2.791765, 2.793137, 2.79451, 2.795882, 2.797255, 2.798628, 2.8, 2.801373, 2.802745, 2.804118, 2.807206, 2.810294, 2.813382, 2.816471, 2.81853, 2.820588, 2.822647, 2.824706, 2.826765, 2.828824, 2.830883, 2.832941, 2.835, 2.837059, 2.839118, 2.841177, 2.844265, 2.847353, 2.850441, 2.853529, 2.855588, 2.857647, 2.859706, 2.861765, 2.863824, 2.865882, 2.868971, 2.872059, 2.875147, 2.878235, 2.88, 2.881765, 2.883529, 2.885294, 2.887059, 2.888824, 2.890588, 2.892647, 2.894706, 2.896765, 2.898824, 2.900883, 2.902941, 2.905, 2.907059, 2.909118, 2.911177, 2.913235, 2.915294, 2.917353, 2.919412, 2.921471, 2.92353, 2.925588, 2.927647, 2.929706, 2.931765, 2.933824, 2.935883, 2.937941, 2.94, 2.941544, 2.943088, 2.944633, 2.946177, 2.947721, 2.949265, 2.950809, 2.952353, 2.954412, 2.956471, 2.958529, 2.960588, 2.962647, 2.964706, 2.970882, 2.977059, 2.978432, 2.979804, 2.981177, 2.982549, 2.983922, 2.985294, 2.986667, 2.988039, 2.989412, 2.991177, 2.992941, 2.994706, 2.996471, 2.998235, 3.0, 3.001765, 3.004853, 3.007941, 3.011029, 3.014118, 3.015882, 3.017647, 3.019412, 3.021177, 3.022941, 3.024706, 3.026471, 3.028235, 3.03, 3.031765, 3.03353, 3.035294, 3.037059, 3.038824, 3.040368, 3.041912, 3.043456, 3.045, 3.046544, 3.048088, 3.049633, 3.051177, 3.053236, 3.055294, 3.057353, 3.059412, 3.061471, 3.063529, 3.065294, 3.067059, 3.068824, 3.070588, 3.072353, 3.074118, 3.075882, 3.077647, 3.079412, 3.081177, 3.082941, 3.084706, 3.086471, 3.088235, 3.08978, 3.091324, 3.092868, 3.094412, 3.095956, 3.0975, 3.099044, 3.100588, 3.102647, 3.104706, 3.106765, 3.108824, 3.110882, 3.112941, 3.114486, 3.11603, 3.117574, 3.119118, 3.120662, 3.122206, 3.12375, 3.125294, 3.128382, 3.131471, 3.134559, 3.137647, 3.13902, 3.140392, 3.141765, 3.143137, 3.14451, 3.145883, 3.147255, 3.148628, 3.15, 3.15, 3.15, 3.15, 3.15]

    NOM_RES = 10000
    SER_RES = 9820
    TEMP_NOM = 25
    NUM_SAMPLES = 25
    THERM_B_COEFF = 3950
    ADC_MAX = 1023
    ADC_VMAX = 3.3

    def __init__(self, TENP_SENS_ADC_PIN_NO = 32):
        self.temp_sens = self.init_temp_sensor(TENP_SENS_ADC_PIN_NO)


    def init_temp_sensor(self, TENP_SENS_ADC_PIN_NO):
        adc = ADC(Pin(TENP_SENS_ADC_PIN_NO))
        adc.atten(ADC.ATTN_11DB)
        adc.width(ADC.WIDTH_10BIT)
        return adc

    def read_temp(self):
        raw_read = []
        # Collect NUM_SAMPLES
        for i in range(1, self.NUM_SAMPLES+1):
            raw_read.append(self.temp_sens.read())

        # Average of the NUM_SAMPLES and look it up in the table
        raw_average = sum(raw_read)/self.NUM_SAMPLES

        # Convert to resistance
        raw_average = self.ADC_MAX * self.adc_V_lookup[round(raw_average)]/self.ADC_VMAX
        resistance = (self.SER_RES * raw_average) / (self.ADC_MAX - raw_average)
        # Convert to temperature
        steinhart  = log(resistance / self.NOM_RES) / self.THERM_B_COEFF
        steinhart += 1.0 / (self.TEMP_NOM + 273.15)
        steinhart  = (1.0 / steinhart) - 273.15
        return steinhart - 1.4 # Constant is subtracted because of thermometer calibration
